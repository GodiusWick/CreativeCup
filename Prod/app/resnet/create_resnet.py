from typing import Tuple
from .resnet import ResNet, ResNetResidualBlock, ResNetBottleneckBlock


def resnet18(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(2, 2, 2, 2), dropout=dropout)


def resnet20(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(3, 3, 3), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def resnet32(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(5, 5, 5), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def resnet34(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(3, 4, 6, 3), dropout=dropout)


def resnet44(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(7, 7, 7), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def resnet50(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetBottleneckBlock,
                  layers_depths=(3, 4, 6, 3), dropout=dropout)


def resnet56(in_channels: int,
             n_classes: int,
             dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(9, 9, 9), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def resnet101(in_channels: int,
              n_classes: int,
              dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetBottleneckBlock,
                  layers_depths=(3, 4, 23, 3), dropout=dropout)


def resnet110(in_channels: int,
              n_classes: int,
              dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(18, 18, 18), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def resnet152(in_channels: int,
              n_classes: int,
              dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetBottleneckBlock,
                  layers_depths=(3, 8, 36, 3), dropout=dropout)


def resnet1202(in_channels: int,
               n_classes: int,
               dropout: int = 0):
    return ResNet(in_channels, n_classes, block=ResNetResidualBlock,
                  layers_depths=(200, 200, 200), blocks_sizes=(16, 32, 64),
                  gate_kernel_size=3, gate_stride=1, gate_padding=1,
                  maxpool=False, dropout=dropout)


def create_resnet(in_channels: int,
                  n_classes: int,
                  block: str,
                  layers_depths: Tuple[int, ...],
                  blocks_sizes: Tuple[int, ...],
                  gate_kernel_size: int,
                  gate_stride: int,
                  gate_padding: int,
                  maxpool: bool,
                  dropout: int,
                  layers_strides: Tuple[int, ...]):
    if block == "ResidualBlock":
        block = ResNetResidualBlock
    elif block == "BottleneckBlock":
        block = ResNetBottleneckBlock
    else:
        raise ValueError("Unrecognized ResNet block type: " + block)

    return ResNet(in_channels, n_classes, block=block,
                  layers_depths=layers_depths, blocks_sizes=blocks_sizes,
                  gate_kernel_size=gate_kernel_size, gate_stride=gate_stride,
                  gate_padding=gate_padding, maxpool=maxpool, dropout=dropout,
                  layers_strides=layers_strides)
