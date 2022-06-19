using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;

public class TestTCP : MonoBehaviour
{
    float m_Timer;
    bool m_DebugMode = false;

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
                if (m_DebugMode) Debug.Log("1) before method");
                MyAsync();
                if (m_DebugMode) Debug.Log("3) after method");
            }
            catch
            {
                if (m_DebugMode) Debug.Log("Error: was catched");
                m_Timer = Time.time;
            }
        }
    }

    async void MyAsync()
    {
        byte[] mes = System.Text.Encoding.ASCII.GetBytes("{key1_update:val1_true, key2:val2}"); // string someString = Encoding.ASCII.GetString(bytes);
        if (m_DebugMode) Debug.Log("2) before sending");
        try
        {
            int x = await Task.Run(() => MyTCPClientLibrary.Send(mes));
            if (x == 1)
            {
                Debug.Log("reset happend");

                var node = GameObject.Find("node_00");
                var nodes = node.GetComponentsInChildren<InKin.RobotJoint>();
                Debug.Log("node=" + node);
                Debug.Log("nodes count=" + nodes.Length);
                foreach (InKin.RobotJoint j in nodes)
                {
                    Debug.Log("joint:" + j.name);
                    j.transform.localEulerAngles = Vector3.zero;
                }
            }
        }
        catch
        {
            if (m_DebugMode) Debug.Log("Task.Run error was catched");
        }
        //int x = await Task.Run(() => My());
        

        if (m_DebugMode) Debug.Log("4) after sending");
    }
    
}
