from typing import Tuple
import torch.nn as nn
from collections import OrderedDict


def create_node(in_channels: int,
                out_channels: int,
                conv: nn.Module = nn.Conv2d,
                activation: nn.Module = None,
                dropout: float = .0,
                **kwargs):
    if activation is None:
        return nn.Sequential(OrderedDict({
            'conv': conv(in_channels, out_channels, **kwargs),
            'batch_normal': nn.BatchNorm2d(out_channels),
            'dropout': nn.Dropout2d(p=dropout)
        }))
    else:
        return nn.Sequential(OrderedDict({
            'conv': conv(in_channels, out_channels, **kwargs),
            'batch_normal': nn.BatchNorm2d(out_channels),
            'dropout': nn.Dropout2d(p=dropout),
            'activation': activation()
        }))


class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 stride: Tuple[int, int],
                 expansion: int,
                 activation: nn.Module):
        super(ResidualBlock, self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.stride = stride
        self.expansion = expansion
        self.nodes = nn.Identity()
        self.activation = activation()
        self.downsample = create_node(
            self.in_channels, self.out_channels * self.expansion,
            kernel_size=1, stride=stride, padding=0, bias=False
        ) if self.stride != 1 or self.in_channels != self.out_channels * self.expansion else nn.Identity()

    def forward(self, x):
        residue = self.downsample(x)
        x = self.nodes(x)
        x += residue
        x = self.activation(x)
        return x


class ResNetResidualBlock(ResidualBlock):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 stride: Tuple[int, int] = (1, 1),
                 expansion: int = 1,
                 activation: nn.Module = nn.ReLU,
                 dropout: float = .0):
        super(ResNetResidualBlock, self).__init__(in_channels, out_channels, stride, expansion, activation)
        self.nodes = nn.Sequential(OrderedDict({
            'node_1': create_node(self.in_channels, self.out_channels,
                                  activation=activation, dropout=dropout,
                                  kernel_size=3, stride=stride, padding=1, bias=False),
            'node_2': create_node(self.out_channels, self.out_channels,
                                  dropout=dropout, kernel_size=3, stride=1, padding=1, bias=False)
        }))


class ResNetBottleneckBlock(ResidualBlock):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 stride: Tuple[int, int] = (1, 1),
                 expansion: int = 4,
                 activation: nn.Module = nn.ReLU,
                 dropout: float = .0):
        super(ResNetBottleneckBlock, self).__init__(in_channels, out_channels, stride, expansion, activation)
        self.nodes = nn.Sequential(OrderedDict({
            'node_1': create_node(self.in_channels, self.out_channels,
                                  activation=activation, dropout=dropout,
                                  kernel_size=1, stride=1, padding=0, bias=False),
            'node_2': create_node(self.out_channels, self.out_channels,
                                  activation=activation, dropout=dropout,
                                  kernel_size=3, stride=stride, padding=1, bias=False),
            'node_3': create_node(self.out_channels, self.out_channels * self.expansion,
                                  dropout=dropout, kernel_size=1, stride=1, padding=0, bias=False)
        }))


class ResNetLayer(nn.Module):
    def __init__(self, in_channels: int,
                 out_channels: int,
                 block: ResidualBlock,
                 layer_depth: Tuple[int, ...],
                 stride: Tuple[int, int] = (1, 1),
                 expansion: int = 1,
                 activation: nn.Module = nn.ReLU,
                 dropout: float = .0):
        super(ResNetLayer, self).__init__()
        self.blocks = nn.Sequential(OrderedDict({
            'blocks_1': block(in_channels, out_channels, stride=stride, expansion=expansion,
                              activation=activation, dropout=dropout),
            **{'block_' + str(i): block(out_channels * expansion, out_channels, dropout=dropout)
               for i in range(2, layer_depth + 1)}
        }))

    def forward(self, x):
        return self.blocks(x)


class ResNetEncoder(nn.Module):
    def __init__(self, in_channels,
                 block: ResidualBlock = ResNetResidualBlock,
                 blocks_sizes: Tuple[int, ...] = (64, 128, 256, 512),
                 layers_depths: Tuple[int, ...] = (2, 2, 2, 2),
                 activation: nn.Module = nn.ReLU,
                 gate_kernel_size: int = 7,
                 gate_stride: int = 2,
                 gate_padding: int = 3,
                 maxpool: bool = True,
                 dropout: float = .0,
                 layers_strides: Tuple[int, ...] = (1, 2, 2, 2)):
        super(ResNetEncoder, self).__init__()
        if maxpool:
            self.gate = nn.Sequential(OrderedDict({
                'node': create_node(in_channels, blocks_sizes[0], activation=activation,
                                    dropout=dropout, kernel_size=gate_kernel_size, stride=gate_stride,
                                    padding=gate_padding, bias=False),
                'max_pool': nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
            }))
        else:
            self.gate = create_node(in_channels, blocks_sizes[0], activation=activation,
                                    dropout=dropout, kernel_size=gate_kernel_size, stride=gate_stride,
                                    padding=gate_padding, bias=False)
        if block == ResNetResidualBlock:
            self.layers = nn.Sequential(OrderedDict({
                **{'layer_' + str(i + 1): ResNetLayer(blocks_sizes[i - 1 if i > 0 else 0],
                                                      blocks_sizes[i], block, layers_depths[i],
                                                      stride=layers_strides[i], expansion=1,
                                                      activation=activation, dropout=dropout)
                   for i in range(len(layers_depths))}
            }))
        else:
            self.layers = nn.Sequential(OrderedDict({
                **{'layer_' + str(i + 1): ResNetLayer(blocks_sizes[i] if i == 0 else blocks_sizes[i] * 2,
                                                      blocks_sizes[i], block, layers_depths[i],
                                                      stride=layers_strides[i], expansion=4,
                                                      activation=activation, dropout=dropout)
                   for i in range(len(layers_depths))}
            }))

    def forward(self, x):
        x = self.gate(x)
        x = self.layers(x)
        return x


class ResNetDecoder(nn.Module):
    def __init__(self, in_data: int,
                 n_classes: int):
        super(ResNetDecoder, self).__init__()
        self.average_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.linear = nn.Linear(in_data, n_classes)

    def forward(self, x):
        x = self.average_pool(x)
        x = x.reshape(x.size(0), -1)
        x = self.linear(x)
        return x


class ResNet(nn.Module):
    def __init__(self, in_channels: int,
                 n_classes: int,
                 **kwargs):
        super(ResNet, self).__init__()
        self.encoder = ResNetEncoder(in_channels, **kwargs)
        self.decoder = ResNetDecoder(self.encoder.layers[-1].blocks[-1].out_channels
                                     * self.encoder.layers[-1].blocks[-1].expansion, n_classes)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
