using System.Security.Cryptography;
using UnityEngine;
using UnityEngine.InputSystem;
public class PlayerBehaviour : MonoBehaviour
{
    public float speed = 5.0f;
    private Camera mainCamera;
    private Rigidbody2D rb;
    private Vector3 lastPosition; 
    public float skillCooldown = 5f; 
    private float lastSkillUseTime;
    private int skillUses = 0;
    private HUDManager hudManager;
    private int health = 100;
    public ParticleSystem skillEffect;
    public AudioSource walkingSound;
    private InputController inputActions; 
    private Vector2 movementInput;
    private Animator animator;

    void Awake()
    {
        mainCamera = Camera.main;
        hudManager = FindObjectOfType<HUDManager>();
        animator = GetComponentInChildren<Animator>();

        inputActions = new InputController();


        inputActions.mainmap.UpDown.performed += ctx => movementInput.y = ctx.ReadValue<float>();
        inputActions.mainmap.UpDown.canceled += ctx => movementInput.y = 0;
        inputActions.mainmap.LeftRight.performed += ctx => movementInput.x = ctx.ReadValue<float>();
        inputActions.mainmap.LeftRight.canceled += ctx => movementInput.x = 0;

        inputActions.mainmap.SkillUse.performed += ctx => UseSkill();

        inputActions.Enable();
    }


    void OnDisable()
    {
        inputActions.Disable();
    }
    void Start()
    {
        rb = GetComponent<Rigidbody2D>(); 
        mainCamera = Camera.main; 
        lastPosition = transform.position; 
        hudManager = FindObjectOfType<HUDManager>(); 
        PlayerPrefs.SetInt("slainEnemies", 0);
    }

    void Update()
    {
        Vector3 movement = new Vector3(movementInput.x, movementInput.y) * speed * Time.deltaTime;
        transform.position += movement;

        checkFlip();
        if (movement.magnitude > 0 && !walkingSound.isPlaying)
        {
            walkingSound.Play();
            animator.SetBool("isWalking", true);
        }
        else if (movement.magnitude == 0 && walkingSound.isPlaying)
        {
            walkingSound.Stop();
            animator.SetBool("isWalking", false);
        }
            

        if (mainCamera && transform.position != lastPosition)
            mainCamera.transform.position = new Vector3(transform.position.x, transform.position.y, mainCamera.transform.position.z);


        lastPosition = transform.position;
    }

    void checkFlip()
    {
        if (movementInput.x > 0)
        {
            transform.localScale = new Vector3(1, 1, 1);
        }
        else if (movementInput.x < 0)
        {
            transform.localScale = new Vector3(-1, 1, 1);
        }

    }

    private void OnCollisionStay2D(UnityEngine.Collision2D collision)
    {
        if (collision.gameObject.tag == "Enemy")
        {
            TakeDamage(1);
        }
    }


    void UseSkill()
    {
        if (Time.time - lastSkillUseTime < skillCooldown || skillUses <= 0) return;
        GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");

        skillEffect.Play(); 

        foreach (var enemy in enemies)
        {
            if (Vector2.Distance(transform.position, enemy.transform.position) <= 3)
            {
                Destroy(enemy);
                PlayerPrefs.SetInt("slainEnemies", PlayerPrefs.GetInt("slainEnemies") + 1);
            }
        }
        DecreaseSkillUses(1);
        lastSkillUseTime = Time.time;
    }

    public void IncreaseSkillUses(int uses)
    {
        skillUses += uses;
        hudManager.UpdateSkillUses(skillUses);
    }

    public void DecreaseSkillUses(int uses)
    {
        skillUses -= uses;
        hudManager.UpdateSkillUses(skillUses, true);
    }

    public void TakeDamage(int damage)
    {
        health -= damage;
        hudManager.UpdateHealth(health);
    }
}
