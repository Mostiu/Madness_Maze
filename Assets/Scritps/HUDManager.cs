using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using UnityEngine.UIElements;
using UnityEngine.UI;

public class HUDManager : MonoBehaviour
{
    public TextMeshProUGUI timeText;
    public TextMeshProUGUI skillUsesText;
    public TextMeshProUGUI healthText;
    private AudioSource backgroundMusic;
    private bool isMusicPaused = false;
    private float elapsedTime = 0f;
    public TextMeshProUGUI musicTextButton;
    void Start()
    {
        backgroundMusic = GameObject.Find("Background").GetComponent<AudioSource>();
        UpdateHealth(100);
        UpdateSkillUses(0);
    }
    void Update()
    {
        elapsedTime += Time.deltaTime;
        UpdateTimeDisplay();
    }

    void UpdateTimeDisplay()
    {
        timeText.text = "Time: " + Mathf.FloorToInt(elapsedTime / 60).ToString("00") + ":" + Mathf.FloorToInt(elapsedTime % 60).ToString("00");
    }

    public void UpdateSkillUses(int uses, bool cooldown=false)
    { 
        skillUsesText.text = "Holy Skill: " + uses;
        if (cooldown)
        {
            StartCoroutine(ChangeSkillTextColorTemporarily());
        }
        
    }

    IEnumerator ChangeSkillTextColorTemporarily()
    {
        skillUsesText.color = Color.red; 
        yield return new WaitForSeconds(5f); 
        skillUsesText.color = Color.white; 
    }

    public void UpdateHealth(int health)
    {
        healthText.text = "Health: " + health;
        if (health <= 0)
        {
            OnPlayerDeath();
        }
    }

    public void OnPlayerDeath()
    {
        SceneController sceneController = FindObjectOfType<SceneController>();
        PlayerPrefs.SetFloat("time", elapsedTime);
        if (sceneController != null)
        {
            sceneController.GoToEnd();
        }
    }


    public void ToggleMusic()
    {
        if (backgroundMusic == null) return;

        if (isMusicPaused)
        {
            backgroundMusic.Play();
            musicTextButton.text = "Pause Music";
            isMusicPaused = false;
        }
        else
        {
            backgroundMusic.Pause();
            musicTextButton.text = "Play Music";
            isMusicPaused = true;
        }
    }
}
