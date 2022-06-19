using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestTCP : MonoBehaviour
{
    float m_Timer;

    private void Start()
    {
        m_Timer = Time.time;
    }

    void Update()
    {
        //if (true || Input.GetKeyDown(KeyCode.Space))
        //if (Input.GetKeyDown(KeyCode.Space))
        if (Time.time - m_Timer > 1) // sanity check each second
        {
            try
            {
                m_Timer = Time.time;
                //byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1:val1, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
                //                                                                            //MyTCPClientLibrary.Send(mes);
                //await MyTCPClientLibrary.Send(mes);
                Debug.Log("1) before method");
                MyAsync();
                Debug.Log("3) after method");
            }
            catch
            {
                Debug.Log("Error: was catched");
                m_Timer = Time.time;
            }
        }
    }

    async void MyAsync()
    {
        byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1_update:val1_true, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
        Debug.Log("2) before sending");
        try
        {
            int x = await Task.Run(() => MyTCPClientLibrary.Send(mes));
        }
        catch
        {
            Debug.Log("Task.Run error was catched");
        }
        //int x = await Task.Run(() => My());
        Debug.Log("4) after sending");
    }
    
}
