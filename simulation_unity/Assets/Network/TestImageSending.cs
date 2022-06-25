using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestImageSending : MonoBehaviour
{

    public Texture2D Tex;
    public bool BigMessage;
     

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log("1) before method");
            MyAsync();
            Debug.Log("3) after method");
        }
    }

    async void MyAsync()
    {
        //string txt = 
        string txt = !BigMessage ? "tester" : MyTCPClientLibrary.ImageToString(Tex); ;
        byte[] mes = System.Text.Encoding.ASCII.GetBytes(txt); // string someString = Encoding.ASCII.GetString(bytes);
        Debug.Log("2) before sending");
        string x = await Task.Run(() => MyTCPClientLibrary.SendAndReceive(mes));
        //int x = await Task.Run(() => My());
        Debug.Log("4) after sending");
    }
}
