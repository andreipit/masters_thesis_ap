using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestTCP : MonoBehaviour
{
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            //byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1:val1, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
            //                                                                            //MyTCPClientLibrary.Send(mes);
            //await MyTCPClientLibrary.Send(mes);
            Debug.Log("1) before method");
            MyAsync();
            Debug.Log("3) after method");
        }
    }

    async void MyAsync()
    {
        byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1:val1, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
        Debug.Log("2) before sending");
		int x = await Task.Run(() => MyTCPClientLibrary.Send(mes));
		//int x = await Task.Run(() => My());
        Debug.Log("4) after sending");
    }
    
}
