using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CollectibleController : MonoBehaviour
{

    private PlayerBehaviour player;

    void Start()
    {
        player = FindObjectOfType<PlayerBehaviour>();
    }

    void Update()
    {
        
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "Player")
        {
            int skillUses = Random.Range(1, 3); 

            player.IncreaseSkillUses(skillUses);

            Destroy(gameObject);
        }
    }
}
