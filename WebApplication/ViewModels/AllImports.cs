using System;
using System.Collections.Generic;
using WebApplication.Models;

namespace WebApplication.ViewModels
{
    public class AllImports
    {
        public Dictionary<int, Import> allIports { get; set; }
        public string[] statuses { get; set; }
    }
}
