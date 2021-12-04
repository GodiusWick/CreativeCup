using System;
using System.IO;
using System.Net;

namespace WebApplication.Web
{
    public class HttpWebRequests
    {
        string uri = "http://192.168.43.11:49161/";

        public HttpWebRequests(string path)
        {
            uri += path;
        }

        public string Request(string contentType, string body, Method method)
        {
            try
            {
                WebRequest request = WebRequest.Create(uri);
                request.Method = method.ToString();

                byte[] byteArray = System.Text.Encoding.ASCII.GetBytes(body);

                request.ContentType = contentType;
                request.ContentLength = byteArray.Length;

                using (Stream dataStream = request.GetRequestStream())
                {
                    dataStream.Write(byteArray, 0, byteArray.Length);
                }

                string json = "";

                WebResponse response = request.GetResponse();
                using (Stream stream = response.GetResponseStream())
                {
                    using (StreamReader reader = new StreamReader(stream))
                    {
                        json = reader.ReadToEnd();
                    }
                }

                response.Close();
                Console.WriteLine("Запрос выполнен...");

                return json;
            }
            catch(Exception ex)
            {
                Console.WriteLine(ex.ToString());
                return ex.ToString();
            }
            
        }

        public enum Method
        {
            POST,
            GET
        }
    }
}
