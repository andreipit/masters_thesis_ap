using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestAsyncAwait : MonoBehaviour
{
    public string Box = "";
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Box = "3";
            Debug.Log("before fun = " + Box);
            MyAsync();
            Debug.Log("after fun = " + Box);
            // output: 
            /*
            => before fun = 3
            => after fun = 1
            pause ~ 1 sec
            => after server response = 777.
            no pause
            => after sending = 2777
            */
        }
    }

    async void MyAsync()
    {
        Box = "1";
        int x = await Task.Run(() => My());
        Box = "2" + x.ToString();
        Debug.Log("after sending = " + Box);
    }

    int My()
    {
        Thread.Sleep(1000);
        Box = "777";
        Debug.Log("after server response = " + Box);
        return 777;
    }

}



//async Task<int> FromSite() 
//   {
//	var client = new HttpClient();
//	int x = (await client.GetStringAsync("http//ya.ru")).length);
//	return x;
//   }