examples = [
    {
        "example_query": "How would you find the missing number in a given integer array of 1 to 100?",
        "example_response": '[{{"content":"To find the missing number in an array that should contain numbers 1 to 100, you can calculate the expected sum of numbers from 1 to 100 using the formula (n * (n + 1)) / 2, where n is 100. Then, subtract the actual sum of numbers in the array from this expected sum. The difference is the missing number."}}]'
    },
    {
        "example_query": "Write a function to reverse a string in Python.",
        "example_response": '[{{"content":"To reverse a string in Python, you can use the slicing method. Define a function that takes a string as an input and returns the string[::-1]. This slices the string starting from the end towards the first character, thus reversing it."}}]'
    },
    {
        "example_query": "How would you design a URL shortening service like bit.ly?",
        "example_response": '[{{"content":"Designing a URL shortening service requires a system that can map long URLs to short, unique identifiers. Key components include a RESTful API for URL submission and redirection, a database for storing URL mappings, and an algorithm for generating short, unique identifiers. Scalability, high availability, and low latency are important factors to consider in the design."}}]'
    },
    {
        "example_query": "Write a function to calculate the number of ways to climb a staircase if you can take 1, 2, or 3 steps at a time.",
        "example_response": '[{{"content":"This problem can be solved using dynamic programming. Create a function that takes the total number of steps as input and uses a dynamic array to store the number of ways to reach each step. The base cases are: 1 way to climb 1 step, 2 ways for 2 steps, and 4 ways for 3 steps. For each subsequent step, the number of ways to climb is the sum of the ways to climb the previous three steps."}}]'
    },
    {
        "example_query": "How would you implement Dijkstra's algorithm to find the shortest path in a graph?",
        "example_response": '[{{"content":"Dijkstras algorithm can be implemented using a priority queue to keep track of the minimum distance from the start node to each node. Initialize distances to all nodes as infinity and distance to the start node as 0. Extract the node with the smallest distance from the priority queue and update the distances of its adjacent nodes. Repeat until all nodes have been visited or the queue is empty. The algorithm works best with a weighted graph without negative edges."}}]'
    },
    {
        "example_query": "How can you implement a thread-safe singleton pattern in Java?",
        "example_response": '[{{"content":"To implement a thread-safe singleton pattern in Java, you can use the `double-checked locking` principle with a private constructor and a volatile instance variable. Initialize the singleton instance as null. In the getInstance() method, check if the instance is null, and if so, synchronize on a lock. Inside the synchronized block, check again if the instance is null before creating a new instance. This ensures the instance is created only once, even with multiple threads."}}]'
    },
    {
        "example_query": "Design a scalable notification system for a high-traffic web application.",
        "example_response": '[{{"content":"A scalable notification system would use a microservices architecture. Components include a notification service to handle incoming requests, a message queue for buffering and load balancing, and workers for processing notifications. The system should support different types of notifications (email, SMS, push). Scalability can be achieved through load balancers, database sharding, and caching. Monitoring and logging are essential for maintaining system health and performance."}}]'
    },
    {
        "example_query": "What is an efficient algorithm to find all pairs in an array that sum up to a specific target?",
        "example_response": '[{{"content":"An efficient way is to use a hash map to store elements while iterating through the array. For each element, check if the target minus the current element exists in the map. If it does, you have found a pair. Add each element to the map as you iterate. This algorithm has a time complexity of O(n) as it requires only one pass through the array."}}]'
    }
]