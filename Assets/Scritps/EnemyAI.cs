using UnityEngine;

public class EnemyAI : MonoBehaviour
{
    public float speed = 2f;
    private Vector2 movementDirection;
    private Vector2 movementPerSecond;
    private float changeDirectionEverySeconds = 2f;
    private float changeDirectionTimer;

    public LayerMask obstacleLayer; 
    private GameObject player;
    private bool isFollowingPlayer = false;

    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
        CalculateNewDirection();
    }

    void Update()
    {
        if (player == null) return;

        checkFlip();
        DetectPlayer();

        if (!isFollowingPlayer)
        {
            RandomMovement();
        }
        else
        {
            FollowPlayer();
        }
    }

    void checkFlip()
    {
        if (player.transform.position.x > transform.position.x)
        {
            transform.localScale = new Vector3(1, 1, 1);
        }
        else
        {
            transform.localScale = new Vector3(-1, 1, 1);
        }
    }
    void DetectPlayer()
    {
 
        Vector2 directionToPlayer = player.transform.position - transform.position;
        float distanceToPlayer = directionToPlayer.magnitude;

        RaycastHit2D hit = Physics2D.Raycast(transform.position, directionToPlayer.normalized, distanceToPlayer, obstacleLayer);

        if (!hit.collider)
        {
            isFollowingPlayer = true;
        }
        else
        {
            isFollowingPlayer = false;
        }
    }

    void RandomMovement()
    {
        changeDirectionTimer += Time.deltaTime;


        if (changeDirectionTimer >= changeDirectionEverySeconds)
        {
            CalculateNewDirection();
            changeDirectionTimer = 0;
        }

        transform.Translate(movementPerSecond * Time.deltaTime);
    }

    void CalculateNewDirection()
    {

        float angle = Random.Range(0, 360);
        movementDirection = new Vector2(Mathf.Cos(angle * Mathf.Deg2Rad), Mathf.Sin(angle * Mathf.Deg2Rad));
        movementPerSecond = movementDirection * speed;
    }

    void FollowPlayer()
    {
  
        Vector2 directionToPlayer = (player.transform.position - transform.position).normalized;
        transform.Translate(directionToPlayer * speed * Time.deltaTime);
    }

    private void OnDestroy()
    {
        
    }

    private void OnDrawGizmos()
    {

        if (player != null)
        {
            if (isFollowingPlayer)
            {
                Gizmos.color = Color.green;
            }
            else
            {
                Gizmos.color = Color.red;
            }
            Gizmos.DrawLine(transform.position, player.transform.position);
        }
    }
}
