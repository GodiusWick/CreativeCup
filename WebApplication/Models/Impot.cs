using System;
namespace WebApplication.Models
{
    public class Import
    {
        public string id_image { get; set; }
        public string src { get; set; }
        public float lan { get; set; }
        public float log { get; set; }
        public string region { get; set; }
        public int status { get; set; }
        public DateTime timeend { get; set; }
        public DateTime timestart { get; set; }
        public DateTime timeupdate { get; set; }
        public string uuid { get; set; }
    }
}
