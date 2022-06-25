using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.IO;
using System.Threading.Tasks;
using System.Threading;

//public class MyTCPClient : MonoBehaviour
//{
//	void Start()
//	{
//		Debug.Log("start");
//	}

//	void Update()
//	{
//		if (Input.GetKeyDown(KeyCode.Space))
//		{
//			byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1:val1, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
//			MyTCPClientLibrary.Send(mes);
//		}
//	}
//}

public static class MyTCPClientLibrary
{

	#region Public static methods
	
	public static string SendAndReceive(byte[] _Mes)
	{
        //Thread.Sleep(1000);
		var request = CreateRequest();
		SendRequest(request, _Mes);
		string result = GetResponse(request);
		string cleaned = result.Replace("\n", "").Replace("\r", ""); // Remove all newlines from the 'example' string variable
		return cleaned;
	}

	#endregion


	#region Private static methods

	static WebRequest CreateRequest()
	{
		string url = @"http://127.0.0.1:4567";
		var res = WebRequest.Create(url);
		//res.PreAuthenticate = true;
		res.PreAuthenticate = false;
        res.Method = "PUT";
        //res.Method = "GET";
		res.ContentType = "application/json";
		res.Headers.Add("Authorization", "Basic ");
		return res;
	}

	static void SendRequest(WebRequest _Request, byte[] _Mes)
	{
		Stream dataStream = _Request.GetRequestStream();
		dataStream.Write(_Mes, 0, _Mes.Length);
		dataStream.Close();
	}

	static string GetResponse(WebRequest _Request)
	{
		WebResponse response = null;
		try { response = _Request.GetResponse(); }
		catch (System.Exception e) { Debug.Log("Exception: response");  return ""; }
		StreamReader sr = new StreamReader(response.GetResponseStream());
		string result = "";
		while (sr.Peek() != -1)
			try { result += sr.ReadToEnd(); }
			catch (System.ObjectDisposedException e) { Debug.Log("Exception: ReadToEnd"); }
		//Debug.Log("header= " + response.Headers);
		response.Close();
		return result;
	}

	public static string ImageToString(Texture2D _Img)
    {
		string res = "[";
		foreach(var pixel in _Img.GetPixels32())
        {
			res += (pixel + ",");
		}
		res.TrimEnd('!');
		return res;
	}

	#endregion

}


//public static string Send(byte[] _Mes)
//{
//	//Thread.Sleep(1000);
//	var request = CreateRequest();
//	SendRequest(request, _Mes);
//	string result = GetResponse(request);
//	//Debug.Log(result);

//	// Remove all newlines from the 'example' string variable
//	string cleaned = result.Replace("\n", "").Replace("\r", "");
//	return cleaned;
//	//if (cleaned == "html:reset")
//	//      {
//	//          //Debug.Log("reset happend START");
//	//	return 1;
//	//}
//	//return 0;
//}

//import http.server

//class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
//    def do_PUT(self):
//        path: str = self.translate_path(self.path) # C:\Users\user\Desktop\notes\mipt4\repos\xukechun\Recreate_v2\PythonApplication1\PythonApplication1/
//        self.send_response(200)

//		self.send_header('Content-type', 'text/plain')

//		self.end_headers()

//		self.wfile.write("My mes!\n".encode())

//		length: int = int(self.headers['Content-Length'])

//		NewData: str = self.rfile.read(length)
//        #print('in', self.request)
//        print('REQUEST==', NewData)

//def built_in_with_put():
//    http.server.test(HandlerClass = HTTPRequestHandler, port = 4567, bind = '127.0.0.1')

//if __name__ == '__main__':
//    built_in_with_put()


