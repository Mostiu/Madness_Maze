using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
public class SceneController : MonoBehaviour
{
    public void StartGame()
    {
        SceneManager.LoadScene("MainGame");
    }

    public void GoToEnd()
    {
        SceneManager.LoadScene("End");
    }

    public void GoToStart()
    {
        SceneManager.LoadScene("Start");
    }
}
