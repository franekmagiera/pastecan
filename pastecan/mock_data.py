from datetime import datetime

jane_id = '5VkCYbYMDNeJMxhcNmz9'
john_id = '7VFvjCPZjNc6n7VAYuWN'
jane_screen_name = 'JaneDoe'
john_screen_name = 'JohnDoe'

jane = {
    'user_id': jane_id,
    'screen_name': jane_screen_name
}

john = {
    'user_id': john_id,
    'screen_name': john_screen_name
}

mock_users_data = [jane, john]

user1_public = """(define (append list1 list2)
    (if (null? list1)
        list2 
        (cons (car list1) (append (cdr list1) list2))
    )
)
"""

user1_private = "John uses Caesar cipher with shift 3."

user2_public = """(define (gcd a b)
    (if (= b 0)
        a
        (gcd b (remainder a b))
    )
)
"""

user2_private = "Wklv lv pb vhfuhw."

python_content = """from datetime import datetime 
    print(f"Hello on {datetime.today()}")
"""

js_content = """'use strict';
function greet(name) {
    return 'Hello ' + name
}
"""

scala_content = """object Hello {
    def main(args: Array[String]) = {
        println("Hello, world")
    }
}
"""

java_content = """class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!"); 
    }
}
"""

clike_content = """int main(void) {
    printf("Hello, World!\\n");
    return 0;
}
"""

none_content = "Hello everyone!"

mock_pastes_data = [
    {
        'content': python_content,
        'language': 'python',
        'date': datetime(2021, 1, 1, 13, 12),
        'title': 'hello.py',
        'exposure': 'Public'
    },
    {
        'content': js_content,
        'language': 'javascript',
        'date': datetime(2020, 2, 1, 10, 45),
        'title': 'greet.js',
        'exposure': 'Public'
    },
    {
        'content': scala_content,
        'language': 'scala',
        'date': datetime(2019, 3, 1, 6, 12),
        'title': 'Hello.scala',
        'exposure': 'Public'
    },
    {
        'content': java_content,
        'language': 'java',
        'date': datetime(2018, 1, 4, 15, 23),
        'title': 'HelloWorld.java',
        'exposure': 'Public'
    },
    {
        'content': clike_content,
        'language': 'clike',
        'date': datetime(2017, 5, 6, 1, 22),
        'title': 'hi.c',
        'exposure': 'Public'
    },
    {
        'content': none_content,
        'language': 'none',
        'date': datetime(2016, 8, 15, 11, 5),
        'title': 'welcome.txt',
        'exposure': 'Public'
    }
]

mock_user_pastes_data = [
    {
        'content': user1_public,
        'language': 'scheme',
        'date': datetime(2021, 4, 24, 13, 36),
        'title': 'append.scm',
        'exposure': 'Public',
        'user_id': jane_id
    },
    {
        'content': user2_public,
        'language': 'scheme',
        'date': datetime(2021, 4, 25, 7, 33),
        'title': 'gcd.scm',
        'exposure': 'Public',
        'user_id': john_id
    },
    {
        'content': user2_private,
        'language': 'none',
        'date': datetime(2020, 10, 12, 15, 14),
        'title': 'John\'s secret',
        'exposure': 'Private',
        'user_id': john_id
    },
    {
        'content': user1_private,
        'language': 'none',
        'date': datetime(2020, 10, 13, 14, 18),
        'title': 'Jane\'s secret',
        'exposure': 'Private',
        'user_id': jane_id
    }
]
