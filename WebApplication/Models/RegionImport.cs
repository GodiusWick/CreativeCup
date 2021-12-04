using System;
namespace WebApplication.Models
{
    public class RegionImport
    {
        public float lan { get; set; }
        public float lon { get; set; }
        public string region { get; set; }
        public string src { get; set; }
        public int status { get; set; }
        public DateTime timestamp { get; set; }
        public string uuid { get; set; }
    }
}
