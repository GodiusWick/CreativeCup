using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WebApplication.Web;
using WebApplication.Models;
using Newtonsoft.Json;
using WebApplication.ViewModels;

// For more information on enabling MVC for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace WebApplication.Controllers
{
    public class GetItemController : Controller
    {
        public Dictionary<int, Import> Imports { get; set; }
        string[] status = new string[] { "В работе", "Завершено с ошибкой", "Чисто", "Загрязнения", "Отправлено на определение" };
        // GET: /<controller>/
        //[Route("GetImports")]
        public ViewResult Index()
        {
            HttpWebRequests requests = new HttpWebRequests("getImports");

            string ContentType = "application/json";
            string body = "{ \"timestamp\": \"\", \"status\": \"\" }";

            string json = requests.Request(ContentType, body, HttpWebRequests.Method.POST);
            Imports = JsonConvert.DeserializeObject<Dictionary<int, Import>>(json);

            var AllImport = new AllImports
            {
                allIports = Imports,
                statuses = status
            };

            return View(AllImport);
        }

        public ViewResult AboutImport(string id)
        {
            HttpWebRequests requests = new HttpWebRequests("getRegionInfo");

            string ContentType = "application/json";
            string body = "{ \"uuidImport\": \"" + id + "\" }";

            string json = requests.Request(ContentType, body, HttpWebRequests.Method.POST);
            var import = JsonConvert.DeserializeObject<RegionImport>(json);

            var importViewModel = new RegionImportViewModel
            {
                importCart = import,
                statuses = status
            };

            return View("ImportCart", importViewModel);
        }

        //public void Delete
    }
}

