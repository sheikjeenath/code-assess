import os
import sys
import json
from firebase_admin import firestore
# Add backend directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.firebase_service import db

# Define the 15 original DSA problems
problems = [
    {
        "id": "pair-sum",
        "title": "Pair Sum",
        "difficulty": "Easy",
        "tags": ["Array", "Hash Map"],
        "enabled": True,
        "description": (
            "Given a list of integer balances and a target sum, find the indices of the "
            "two balances that sum up to the target.\n\n"
            "Input format:\n"
            "Line 1: A comma-separated list of integers (e.g. `2,7,11,15`)\n"
            "Line 2: The target integer (e.g. `9`)\n\n"
            "Output format:\n"
            "Print the two indices separated by a space, sorted in ascending order (e.g. `0 1`). "
            "If no pair exists, print `-1`."
        ),
        "constraints": [
            "2 <= balances.length <= 10^4",
            "-10^9 <= balances[i] <= 10^9",
            "-10^9 <= target <= 10^9"
        ],
        "starterTemplates": {
            "python": (
                "import sys\n\n"
                "def solve():\n"
                "    lines = sys.stdin.read().splitlines()\n"
                "    if not lines: return\n"
                "    nums = [int(x) for x in lines[0].split(',')]\n"
                "    target = int(lines[1])\n"
                "    # Write your code here\n"
                "    seen = {}\n"
                "    for i, num in enumerate(nums):\n"
                "        comp = target - num\n"
                "        if comp in seen:\n"
                "            print(f\"{seen[comp]} {i}\")\n"
                "            return\n"
                "        seen[num] = i\n"
                "    print(\"-1\")\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            "javascript": (
                "const fs = require('fs');\n\n"
                "function solve() {\n"
                "    const input = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "    if (input.length < 2) return;\n"
                "    const nums = input[0].split(',').map(Number);\n"
                "    const target = Number(input[1]);\n"
                "    const seen = {};\n"
                "    for (let i = 0; i < nums.length; i++) {\n"
                "        const comp = target - nums[i];\n"
                "        if (comp in seen) {\n"
                "            console.log(seen[comp] + ' ' + i);\n"
                "            return;\n"
                "        }\n"
                "        seen[nums[i]] = i;\n"
                "    }\n"
                "    console.log('-1');\n"
                "}\n\n"
                "solve();\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "using namespace std;\n\n"
                "int main() {\n"
                "    string line1, line2;\n"
                "    if (!getline(cin, line1)) return 0;\n"
                "    getline(cin, line2);\n"
                "    int target = stoi(line2);\n"
                "    vector<int> nums;\n"
                "    stringstream ss(line1);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) {\n"
                "        nums.push_back(stoi(val));\n"
                "    }\n"
                "    unordered_map<int, int> seen;\n"
                "    for(int i = 0; i < nums.size(); i++) {\n"
                "        int comp = target - nums[i];\n"
                "        if(seen.count(comp)) {\n"
                "            cout << seen[comp] << \" \" << i << endl;\n"
                "            return 0;\n"
                "        }\n"
                "        seen[nums[i]] = i;\n"
                "    }\n"
                "    cout << -1 << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if (!sc.hasNextLine()) return;\n"
                "        String[] numStrs = sc.nextLine().split(\",\");\n"
                "        int target = sc.nextInt();\n"
                "        int[] nums = new int[numStrs.length];\n"
                "        for (int i = 0; i < numStrs.length; i++) {\n"
                "            nums[i] = Integer.parseInt(numStrs[i].trim());\n"
                "        }\n"
                "        Map<Integer, Integer> seen = new HashMap<>();\n"
                "        for (int i = 0; i < nums.length; i++) {\n"
                "            int comp = target - nums[i];\n"
                "            if (seen.containsKey(comp)) {\n"
                "                System.out.println(seen.get(comp) + \" \" + i);\n"
                "                return;\n"
                "            }\n"
                "            seen.put(nums[i], i);\n"
                "        }\n"
                "        System.out.println(\"-1\");\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "2,7,11,15\n9", "output": "0 1", "explanation": "2 + 7 = 9. Indices 0 and 1 are returned."}
        ],
        "hiddenTestCases": [
            {"input": "2,7,11,15\n9", "output": "0 1", "isSample": True},
            {"input": "3,2,4\n6", "output": "1 2", "isSample": False},
            {"input": "3,3\n6", "output": "0 1", "isSample": False},
            {"input": "1,5,8,12\n20", "output": "2 3", "isSample": False},
            {"input": "1,2,3\n10", "output": "-1", "isSample": False}
        ]
    },
    {
        "id": "first-unique-char",
        "title": "First Unique Character",
        "difficulty": "Easy",
        "tags": ["String", "Hash Map"],
        "enabled": True,
        "description": (
            "Find the index of the first character in a given string that does not repeat anywhere else.\n\n"
            "Input:\n"
            "A single line containing a lowercase alphanumeric string (e.g. `leetcode`).\n\n"
            "Output:\n"
            "Print the 0-indexed index of the character. If all characters repeat, print `-1`."
        ),
        "constraints": ["1 <= s.length <= 10^5", "s consists of lowercase English letters."],
        "starterTemplates": {
            "python": (
                "import sys\n\n"
                "def solve():\n"
                "    s = sys.stdin.read().strip()\n"
                "    counts = {}\n"
                "    for char in s:\n"
                "        counts[char] = counts.get(char, 0) + 1\n"
                "    for i, char in enumerate(s):\n"
                "        if counts[char] == 1:\n"
                "            print(i)\n"
                "            return\n"
                "    print(\"-1\")\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "const counts = {};\n"
                "for (let char of s) {\n"
                "    counts[char] = (counts[char] || 0) + 1;\n"
                "}\n"
                "for (let i = 0; i < s.length; i++) {\n"
                "    if (counts[s[i]] === 1) {\n"
                "        console.log(i);\n"
                "        process.exit(0);\n"
                "    }\n"
                "}\n"
                "console.log('-1');\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <unordered_map>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string s;\n"
                "    if (!(cin >> s)) return 0;\n"
                "    unordered_map<char, int> counts;\n"
                "    for (char c : s) counts[c]++;\n"
                "    for (int i = 0; i < s.length(); i++) {\n"
                "        if (counts[s[i]] == 1) {\n"
                "            cout << i << endl;\n"
                "            return 0;\n"
                "        }\n"
                "    }\n"
                "    cout << -1 << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNext()) return;\n"
                "        String s = sc.next();\n"
                "        Map<Character, Integer> counts = new HashMap<>();\n"
                "        for (int i = 0; i < s.length(); i++) {\n"
                "            char c = s.charAt(i);\n"
                "            counts.put(c, counts.getOrDefault(c, 0) + 1);\n"
                "        }\n"
                "        for (int i = 0; i < s.length(); i++) {\n"
                "            if (counts.get(s.charAt(i)) == 1) {\n"
                "                System.out.println(i);\n"
                "                return;\n"
                "            }\n"
                "        }\n"
                "        System.out.println(\"-1\");\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "codeassess", "output": "0", "explanation": "c is the first unique character."}
        ],
        "hiddenTestCases": [
            {"input": "codeassess", "output": "0", "isSample": True},
            {"input": "loveleetcode", "output": "2", "isSample": False},
            {"input": "aabb", "output": "-1", "isSample": False},
            {"input": "a", "output": "0", "isSample": False},
            {"input": "character", "output": "1", "isSample": False}
        ]
    },
    {
        "id": "array-rotation",
        "title": "Array Rotation",
        "difficulty": "Easy",
        "tags": ["Array"],
        "enabled": True,
        "description": (
            "Rotate an array of integers to the right by $K$ steps.\n\n"
            "Input:\n"
            "Line 1: A comma-separated list of integers.\n"
            "Line 2: The rotation steps integer $K$.\n\n"
            "Output:\n"
            "Print the rotated array as a comma-separated list."
        ),
        "constraints": ["1 <= nums.length <= 10^5", "0 <= k <= 10^5"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "if lines:\n"
                "    nums = lines[0].split(',')\n"
                "    k = int(lines[1]) % len(nums)\n"
                "    rotated = nums[-k:] + nums[:-k] if k > 0 else nums\n"
                "    print(','.join(rotated))\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if(lines.length >= 2) {\n"
                "    const nums = lines[0].split(',');\n"
                "    const k = Number(lines[1]) % nums.length;\n"
                "    const rotated = k > 0 ? [...nums.slice(-k), ...nums.slice(0, -k)] : nums;\n"
                "    console.log(rotated.join(','));\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string l1, l2; if(!getline(cin, l1)) return 0;\n"
                "    getline(cin, l2); int k = stoi(l2);\n"
                "    vector<string> nums;\n"
                "    stringstream ss(l1);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) nums.push_back(val);\n"
                "    int n = nums.size();\n"
                "    k = k % n;\n"
                "    for(int i = 0; i < n; i++) {\n"
                "        cout << nums[(i - k + n) % n];\n"
                "        if(i < n - 1) cout << \",\";\n"
                "    }\n"
                "    cout << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextLine()) return;\n"
                "        String[] nums = sc.nextLine().split(\",\");\n"
                "        int k = sc.nextInt() % nums.length;\n"
                "        String[] rotated = new String[nums.length];\n"
                "        for (int i = 0; i < nums.length; i++) {\n"
                "            rotated[(i + k) % nums.length] = nums[i].trim();\n"
                "        }\n"
                "        System.out.println(String.join(\",\", rotated));\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "1,2,3,4,5\n2", "output": "4,5,1,2,3", "explanation": "Shifted 2 units right."}
        ],
        "hiddenTestCases": [
            {"input": "1,2,3,4,5\n2", "output": "4,5,1,2,3", "isSample": True},
            {"input": "1,2\n3", "output": "2,1", "isSample": False},
            {"input": "10\n5", "output": "10", "isSample": False},
            {"input": "1,2,3,4\n0", "output": "1,2,3,4", "isSample": False},
            {"input": "5,6,7,8\n4", "output": "5,6,7,8", "isSample": False}
        ]
    },
    {
        "id": "valid-palindrome-phrase",
        "title": "Valid Palindrome Phrase",
        "difficulty": "Easy",
        "tags": ["String", "Two Pointers"],
        "enabled": True,
        "description": (
            "Verify if a phrase is a palindrome, ignoring case and removing all non-alphanumeric characters.\n\n"
            "Input:\n"
            "A single line string.\n\n"
            "Output:\n"
            "Print `true` if it is a palindrome, otherwise `false`."
        ),
        "constraints": ["1 <= phrase.length <= 10^5"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "s = sys.stdin.read().strip().lower()\n"
                "cleaned = ''.join(c for c in s if c.isalnum())\n"
                "print('true' if cleaned == cleaned[::-1] else 'false')\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const s = fs.readFileSync('/dev/stdin', 'utf-8').trim().toLowerCase();\n"
                "const cleaned = s.replace(/[^a-z0-9]/g, '');\n"
                "console.log(cleaned === cleaned.split('').reverse().join('') ? 'true' : 'false');\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <cctype>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string s, cleaned = \"\";\n"
                "    getline(cin, s);\n"
                "    for (char c : s) {\n"
                "        if (isalnum(c)) cleaned += tolower(c);\n"
                "    }\n"
                "    int n = cleaned.length();\n"
                "    bool pal = true;\n"
                "    for (int i = 0; i < n/2; i++) {\n"
                "        if (cleaned[i] != cleaned[n - 1 - i]) pal = false;\n"
                "    }\n"
                "    cout << (pal ? \"true\" : \"false\") << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextLine()) { System.out.println(\"true\"); return; }\n"
                "        String s = sc.nextLine().toLowerCase();\n"
                "        StringBuilder sb = new StringBuilder();\n"
                "        for(char c : s.toCharArray()) {\n"
                "            if(Character.isLetterOrDigit(c)) sb.append(c);\n"
                "        }\n"
                "        String clean = sb.toString();\n"
                "        String rev = sb.reverse().toString();\n"
                "        System.out.println(clean.equals(rev) ? \"true\" : \"false\");\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "A man, a plan, a canal: Panama", "output": "true", "explanation": "Resolves to amanaplanacanalpanama."}
        ],
        "hiddenTestCases": [
            {"input": "A man, a plan, a canal: Panama", "output": "true", "isSample": True},
            {"input": "race a car", "output": "false", "isSample": False},
            {"input": " ", "output": "true", "isSample": False},
            {"input": "ab_a", "output": "true", "isSample": False},
            {"input": "No 'x' in Nixon", "output": "true", "isSample": False}
        ]
    },
    {
        "id": "bracket-balancer",
        "title": "Bracket Balancer",
        "difficulty": "Easy",
        "tags": ["Stack", "String"],
        "enabled": True,
        "description": (
            "Determine if a string containing parentheses `()`, brackets `[]`, and braces `{}` is balanced.\n\n"
            "Input:\n"
            "A single line representing the sequence of brackets.\n\n"
            "Output:\n"
            "Print `true` if balanced, otherwise `false`."
        ),
        "constraints": ["1 <= s.length <= 10^4"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "s = sys.stdin.read().strip()\n"
                "stack = []\n"
                "mapping = {')': '(', '}': '{', ']': '['}\n"
                "possible = True\n"
                "for c in s:\n"
                "    if c in mapping:\n"
                "        top = stack.pop() if stack else '#'\n"
                "        if mapping[c] != top:\n"
                "            possible = False\n"
                "            break\n"
                "    else:\n"
                "        stack.append(c)\n"
                "print('true' if possible and not stack else 'false')\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const s = fs.readFileSync('/dev/stdin', 'utf-8').trim();\n"
                "const stack = [];\n"
                "const map = { ')': '(', '}': '{', ']': '[' };\n"
                "let ok = true;\n"
                "for(let c of s) {\n"
                "    if(c in map) {\n"
                "        if(stack.pop() !== map[c]) { ok = false; break; }\n"
                "    } else { stack.push(c); }\n"
                "}\n"
                "console.log(ok && stack.length === 0 ? 'true' : 'false');\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <stack>\n"
                "#include <string>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string s; if(!(cin >> s)) { cout << \"true\" << endl; return 0; }\n"
                "    stack<char> st;\n"
                "    for(char c : s) {\n"
                "        if(c == '(' || c == '{' || c == '[') st.push(c);\n"
                "        else {\n"
                "            if(st.empty()) { cout << \"false\" << endl; return 0; }\n"
                "            if(c == ')' && st.top() != '(') { cout << \"false\" << endl; return 0; }\n"
                "            if(c == '}' && st.top() != '{') { cout << \"false\" << endl; return 0; }\n"
                "            if(c == ']' && st.top() != '[') { cout << \"false\" << endl; return 0; }\n"
                "            st.pop();\n"
                "        }\n"
                "    }\n"
                "    cout << (st.empty() ? \"true\" : \"false\") << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNext()) { System.out.println(\"true\"); return; }\n"
                "        String s = sc.next();\n"
                "        Stack<Character> stack = new Stack<>();\n"
                "        for(char c : s.toCharArray()) {\n"
                "            if(c == '(' || c == '{' || c == '[') stack.push(c);\n"
                "            else {\n"
                "                if(stack.isEmpty()) { System.out.println(\"false\"); return; }\n"
                "                char top = stack.pop();\n"
                "                if(c == ')' && top != '(') { System.out.println(\"false\"); return; }\n"
                "                if(c == '}' && top != '{') { System.out.println(\"false\"); return; }\n"
                "                if(c == ']' && top != '[') { System.out.println(\"false\"); return; }\n"
                "            }\n"
                "        }\n"
                "        System.out.println(stack.isEmpty() ? \"true\" : \"false\");\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "()[]{}", "output": "true", "explanation": "Standard balanced brackets."}
        ],
        "hiddenTestCases": [
            {"input": "()[]{}", "output": "true", "isSample": True},
            {"input": "(]", "output": "false", "isSample": False},
            {"input": "([)]", "output": "false", "isSample": False},
            {"input": "{[]}", "output": "true", "isSample": False},
            {"input": "[", "output": "false", "isSample": False}
        ]
    },
    {
        "id": "island-count",
        "title": "Island Count",
        "difficulty": "Medium",
        "tags": ["Graph", "Breadth First Search", "Depth First Search"],
        "enabled": True,
        "description": (
            "Given a 2D binary grid representing land ('1') and water ('0'), count the number of islands. "
            "An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.\n\n"
            "Input:\n"
            "Line 1: Dimensions $R$ (rows) and $C$ (columns) separated by space (e.g. `4 5`).\n"
            "Next $R$ lines: Space-separated integers representing the grid values.\n\n"
            "Output:\n"
            "Print a single integer representing the island count."
        ),
        "constraints": ["1 <= R, C <= 50", "grid[i][j] is '0' or '1'."],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "def solve():\n"
                "    input_data = sys.stdin.read().splitlines()\n"
                "    if not input_data: return\n"
                "    R, C = map(int, input_data[0].split())\n"
                "    grid = [line.split() for line in input_data[1:R+1]]\n"
                "    visited = set()\n"
                "    count = 0\n"
                "    def dfs(r, c):\n"
                "        if r < 0 or r >= R or c < 0 or c >= C or grid[r][c] == '0' or (r, c) in visited:\n"
                "            return\n"
                "        visited.add((r, c))\n"
                "        dfs(r+1, c)\n"
                "        dfs(r-1, c)\n"
                "        dfs(r, c+1)\n"
                "        dfs(r, c-1)\n"
                "    for r in range(R):\n"
                "        for c in range(C):\n"
                "            if grid[r][c] == '1' and (r, c) not in visited:\n"
                "                count += 1\n"
                "                dfs(r, c)\n"
                "    print(count)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if (lines.length === 0) return;\n"
                "const [R, C] = lines[0].split(' ').map(Number);\n"
                "const grid = lines.slice(1, R+1).map(l => l.trim().split(' '));\n"
                "const visited = Array.from({length: R}, () => Array(C).fill(false));\n"
                "let count = 0;\n"
                "function dfs(r, c) {\n"
                "    if(r < 0 || r >= R || c < 0 || c >= C || grid[r][c] === '0' || visited[r][c]) return;\n"
                "    visited[r][c] = true;\n"
                "    dfs(r + 1, c);\n"
                "    dfs(r - 1, c);\n"
                "    dfs(r, c + 1);\n"
                "    dfs(r, c - 1);\n"
                "}\n"
                "for(let r = 0; r < R; r++) {\n"
                "    for(let c = 0; c < C; c++) {\n"
                "        if(grid[r][c] === '1' && !visited[r][c]) {\n"
                "            count++;\n"
                "            dfs(r, c);\n"
                "        }\n"
                "    }\n"
                "}\n"
                "console.log(count);\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "using namespace std;\n"
                "int R, C;\n"
                "vector<vector<char>> grid;\n"
                "vector<vector<bool>> visited;\n"
                "void dfs(int r, int c) {\n"
                "    if(r < 0 || r >= R || c < 0 || c >= C || grid[r][c] == '0' || visited[r][c]) return;\n"
                "    visited[r][c] = true;\n"
                "    dfs(r+1, c);\n"
                "    dfs(r-1, c);\n"
                "    dfs(r, c+1);\n"
                "    dfs(r, c-1);\n"
                "}\n"
                "int main() {\n"
                "    if(!(cin >> R >> C)) return 0;\n"
                "    grid.resize(R, vector<char>(C));\n"
                "    visited.resize(R, vector<bool>(C, false));\n"
                "    for(int i = 0; i < R; i++) {\n"
                "        for(int j = 0; j < C; j++) cin >> grid[i][j];\n"
                "    }\n"
                "    int count = 0;\n"
                "    for(int i = 0; i < R; i++) {\n"
                "        for(int j = 0; j < C; j++) {\n"
                "            if(grid[i][j] == '1' && !visited[i][j]) {\n"
                "                count++;\n"
                "                dfs(i, j);\n"
                "            }\n"
                "        }\n"
                "    }\n"
                "    cout << count << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    static int R, C;\n"
                "    static String[][] grid;\n"
                "    static boolean[][] visited;\n"
                "    static void dfs(int r, int c) {\n"
                "        if (r < 0 || r >= R || c < 0 || c >= C || grid[r][c].equals(\"0\") || visited[r][c]) return;\n"
                "        visited[r][c] = true;\n"
                "        dfs(r+1, c);\n"
                "        dfs(r-1, c);\n"
                "        dfs(r, c+1);\n"
                "        dfs(r, c-1);\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if (!sc.hasNextInt()) return;\n"
                "        R = sc.nextInt();\n"
                "        C = sc.nextInt();\n"
                "        grid = new String[R][C];\n"
                "        visited = new boolean[R][C];\n"
                "        for (int i = 0; i < R; i++) {\n"
                "            for (int j = 0; j < C; j++) {\n"
                "                grid[i][j] = sc.next();\n"
                "            }\n"
                "        }\n"
                "        int count = 0;\n"
                "        for (int i = 0; i < R; i++) {\n"
                "            for (int j = 0; j < C; j++) {\n"
                "                if (grid[i][j].equals(\"1\") && !visited[i][j]) {\n"
                "                    count++;\n"
                "                    dfs(i, j);\n"
                "                }\n"
                "            }\n"
                "        }\n"
                "        System.out.println(count);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "output": "1", "explanation": "Single connected block of land."}
        ],
        "hiddenTestCases": [
            {"input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "output": "1", "isSample": True},
            {"input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1", "output": "3", "isSample": False},
            {"input": "1 1\n0", "output": "0", "isSample": False},
            {"input": "1 1\n1", "output": "1", "isSample": False},
            {"input": "3 3\n1 0 1\n0 1 0\n1 0 1", "output": "5", "isSample": False}
        ]
    },
    {
        "id": "merge-intervals",
        "title": "Merge Interval Lists",
        "difficulty": "Medium",
        "tags": ["Sorting", "Array"],
        "enabled": True,
        "description": (
            "Given a list of intervals, merge all overlapping intervals.\n\n"
            "Input:\n"
            "Line 1: Number of intervals $N$.\n"
            "Next $N$ lines: Space-separated start and end values (e.g. `1 3`).\n\n"
            "Output:\n"
            "Print the merged intervals, one per line, formatted as `start end`."
        ),
        "constraints": ["1 <= N <= 10^4", "start <= end"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "if lines:\n"
                "    N = int(lines[0])\n"
                "    intervals = []\n"
                "    for l in lines[1:N+1]:\n"
                "        intervals.append(list(map(int, l.split())))\n"
                "    intervals.sort(key=lambda x: x[0])\n"
                "    merged = []\n"
                "    for interval in intervals:\n"
                "        if not merged or merged[-1][1] < interval[0]:\n"
                "            merged.append(interval)\n"
                "        else:\n"
                "            merged[-1][1] = max(merged[-1][1], interval[1])\n"
                "    for m in merged:\n"
                "        print(f\"{m[0]} {m[1]}\")\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if (lines.length > 0) {\n"
                "    const N = Number(lines[0]);\n"
                "    const intervals = [];\n"
                "    for (let i = 1; i <= N; i++) {\n"
                "        intervals.push(lines[i].split(' ').map(Number));\n"
                "    }\n"
                "    intervals.sort((a,b) => a[0] - b[0]);\n"
                "    const merged = [];\n"
                "    for(let item of intervals) {\n"
                "        if(merged.length === 0 || merged[merged.length-1][1] < item[0]) {\n"
                "            merged.push(item);\n"
                "        } else {\n"
                "            merged[merged.length-1][1] = Math.max(merged[merged.length-1][1], item[1]);\n"
                "        }\n"
                "    }\n"
                "    for(let m of merged) {\n"
                "        console.log(m[0] + ' ' + m[1]);\n"
                "    }\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    int N;\n"
                "    if (!(cin >> N)) return 0;\n"
                "    vector<pair<int, int>> intervals(N);\n"
                "    for (int i = 0; i < N; i++) {\n"
                "        cin >> intervals[i].first >> intervals[i].second;\n"
                "    }\n"
                "    sort(intervals.begin(), intervals.end());\n"
                "    vector<pair<int, int>> merged;\n"
                "    for (auto& item : intervals) {\n"
                "        if (merged.empty() || merged.back().second < item.first) {\n"
                "            merged.push_back(item);\n"
                "        } else {\n"
                "            merged.back().second = max(merged.back().second, item.second);\n"
                "        }\n"
                "    }\n"
                "    for (auto& m : merged) {\n"
                "        cout << m.first << \" \" << m.second << endl;\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextInt()) return;\n"
                "        int N = sc.nextInt();\n"
                "        int[][] intervals = new int[N][2];\n"
                "        for (int i = 0; i < N; i++) {\n"
                "            intervals[i][0] = sc.nextInt();\n"
                "            intervals[i][1] = sc.nextInt();\n"
                "        }\n"
                "        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));\n"
                "        List<int[]> merged = new ArrayList<>();\n"
                "        for (int[] interval : intervals) {\n"
                "            if (merged.isEmpty() || merged.get(merged.size() - 1)[1] < interval[0]) {\n"
                "                merged.add(interval);\n"
                "            } else {\n"
                "                merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]);\n"
                "            }\n"
                "        }\n"
                "        for (int[] m : merged) {\n"
                "            System.out.println(m[0] + \" \" + m[1]);\n"
                "        }\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "output": "1 6\n8 10\n15 18", "explanation": "[1,3] and [2,6] overlap, merged to [1,6]."}
        ],
        "hiddenTestCases": [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "output": "1 6\n8 10\n15 18", "isSample": True},
            {"input": "2\n1 4\n4 5", "output": "1 5", "isSample": False},
            {"input": "3\n1 5\n2 4\n6 8", "output": "1 5\n6 8", "isSample": False},
            {"input": "1\n5 8", "output": "5 8", "isSample": False},
            {"input": "4\n1 10\n2 3\n4 5\n6 7", "output": "1 10", "isSample": False}
        ]
    },
    {
        "id": "binary-tree-depth",
        "title": "Binary Tree Depth",
        "difficulty": "Easy",
        "tags": ["Binary Tree", "Depth First Search"],
        "enabled": True,
        "description": (
            "Determine the maximum depth of a binary tree given its parent-list representation. "
            "The root node has index `0`. The parent representation is a list of parent indices for each node 0 to N-1. "
            "A parent of `-1` indicates the root.\n\n"
            "Input:\n"
            "A single line containing comma-separated parent indices (e.g. `-1,0,0,1,1,2`).\n\n"
            "Output:\n"
            "Print the maximum depth integer."
        ),
        "constraints": ["1 <= N <= 10^3"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "parents = [int(x) for x in sys.stdin.read().strip().split(',')]\n"
                "n = len(parents)\n"
                "depths = [0] * n\n"
                "def get_depth(i):\n"
                "    if depths[i] != 0: return depths[i]\n"
                "    if parents[i] == -1: depths[i] = 1\n"
                "    else: depths[i] = get_depth(parents[i]) + 1\n"
                "    return depths[i]\n"
                "for idx in range(n): get_depth(idx)\n"
                "print(max(depths))\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const parents = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(',').map(Number);\n"
                "const n = parents.length;\n"
                "const depths = Array(n).fill(0);\n"
                "function getDepth(i) {\n"
                "    if (depths[i] !== 0) return depths[i];\n"
                "    if (parents[i] === -1) depths[i] = 1;\n"
                "    else depths[i] = getDepth(parents[i]) + 1;\n"
                "    return depths[i];\n"
                "}\n"
                "for (let idx = 0; idx < n; idx++) getDepth(idx);\n"
                "console.log(Math.max(...depths));\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "vector<int> parents;\n"
                "vector<int> depths;\n"
                "int getDepth(int i) {\n"
                "    if (depths[i] != 0) return depths[i];\n"
                "    if (parents[i] == -1) depths[i] = 1;\n"
                "    else depths[i] = getDepth(parents[i]) + 1;\n"
                "    return depths[i];\n"
                "}\n"
                "int main() {\n"
                "    string line; if(!getline(cin, line)) return 0;\n"
                "    stringstream ss(line);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) parents.push_back(stoi(val));\n"
                "    int n = parents.size();\n"
                "    depths.resize(n, 0);\n"
                "    int maxDepth = 0;\n"
                "    for (int i = 0; i < n; i++) {\n"
                "        maxDepth = max(maxDepth, getDepth(i));\n"
                "    }\n"
                "    cout << maxDepth << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    static int[] parents;\n"
                "    static int[] depths;\n"
                "    static int getDepth(int i) {\n"
                "        if (depths[i] != 0) return depths[i];\n"
                "        if (parents[i] == -1) depths[i] = 1;\n"
                "        else depths[i] = getDepth(parents[i]) + 1;\n"
                "        return depths[i];\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNext()) return;\n"
                "        String[] strs = sc.next().split(\",\");\n"
                "        int n = strs.length;\n"
                "        parents = new int[n];\n"
                "        depths = new int[n];\n"
                "        for (int i = 0; i < n; i++) parents[i] = Integer.parseInt(strs[i].trim());\n"
                "        int maxDepth = 0;\n"
                "        for (int i = 0; i < n; i++) {\n"
                "            maxDepth = Math.max(maxDepth, getDepth(i));\n"
                "        }\n"
                "        System.out.println(maxDepth);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "-1,0,0,1,1,2", "output": "4", "explanation": "Depth calculation path: 2 -> 0 -> root yields depth 4."}
        ],
        "hiddenTestCases": [
            {"input": "-1,0,0,1,1,2", "output": "4", "isSample": True},
            {"input": "-1", "output": "1", "isSample": False},
            {"input": "-1,0,1,2", "output": "4", "isSample": False},
            {"input": "-1,0,0", "output": "2", "isSample": False},
            {"input": "-1,0,0,1,2,2,3", "output": "4", "isSample": False}
        ]
    },
    {
        "id": "kth-smallest-matrix",
        "title": "Kth Smallest Element in Sorted Matrix",
        "difficulty": "Medium",
        "tags": ["Heap", "Binary Search"],
        "enabled": True,
        "description": (
            "Find the $K$-th smallest element in an $N \\times N$ matrix sorted row-wise and column-wise.\n\n"
            "Input:\n"
            "Line 1: Matrix size $N$ and target rank $K$ separated by space.\n"
            "Next $N$ lines: Space-separated integers representing the matrix rows.\n\n"
            "Output:\n"
            "Print the $K$-th smallest element integer."
        ),
        "constraints": ["1 <= N <= 100", "1 <= K <= N^2"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "import heapq\n"
                "def solve():\n"
                "    lines = sys.stdin.read().splitlines()\n"
                "    if not lines: return\n"
                "    N, K = map(int, lines[0].split())\n"
                "    matrix = [list(map(int, line.split())) for line in lines[1:N+1]]\n"
                "    heap = []\n"
                "    for r in range(min(N, K)):\n"
                "        heapq.heappush(heap, (matrix[r][0], r, 0))\n"
                "    val = 0\n"
                "    for _ in range(K):\n"
                "        val, r, c = heapq.heappop(heap)\n"
                "        if c + 1 < N:\n"
                "            heapq.heappush(heap, (matrix[r][c+1], r, c+1))\n"
                "    print(val)\n\n"
                "if __name__ == '__main__':\n"
                "    solve()\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if(lines.length === 0) return;\n"
                "const [N, K] = lines[0].split(' ').map(Number);\n"
                "const matrix = lines.slice(1, N+1).map(l => l.trim().split(' ').map(Number));\n"
                "const list = [];\n"
                "for(let r=0; r<N; r++) {\n"
                "    for(let c=0; c<N; c++) list.push(matrix[r][c]);\n"
                "}\n"
                "list.sort((a,b) => a-b);\n"
                "console.log(list[K-1]);\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <queue>\n"
                "using namespace std;\n"
                "struct Element {\n"
                "    int val, r, c;\n"
                "    bool operator>(const Element& other) const { return val > other.val; }\n"
                "};\n"
                "int main() {\n"
                "    int N, K; if(!(cin >> N >> K)) return 0;\n"
                "    vector<vector<int>> matrix(N, vector<int>(N));\n"
                "    for(int i=0; i<N; i++) {\n"
                "        for(int j=0; j<N; j++) cin >> matrix[i][j];\n"
                "    }\n"
                "    priority_queue<Element, vector<Element>, greater<Element>> pq;\n"
                "    for(int r=0; r<min(N, K); r++) pq.push({matrix[r][0], r, 0});\n"
                "    int val = 0;\n"
                "    for(int i=0; i<K; i++) {\n"
                "        auto top = pq.top(); pq.pop();\n"
                "        val = top.val;\n"
                "        if(top.c + 1 < N) pq.push({matrix[top.r][top.c+1], top.r, top.c+1});\n"
                "    }\n"
                "    cout << val << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    static class Element {\n"
                "        int val, r, c;\n"
                "        Element(int val, int r, int c) {\n"
                "            this.val = val; this.r = r; this.c = c;\n"
                "        }\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextInt()) return;\n"
                "        int N = sc.nextInt();\n"
                "        int K = sc.nextInt();\n"
                "        int[][] matrix = new int[N][N];\n"
                "        for(int i=0; i<N; i++) {\n"
                "            for(int j=0; j<N; j++) matrix[i][j] = sc.nextInt();\n"
                "        }\n"
                "        PriorityQueue<Element> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));\n"
                "        for(int r=0; r<Math.min(N, K); r++) pq.add(new Element(matrix[r][0], r, 0));\n"
                "        int val = 0;\n"
                "        for(int i=0; i<K; i++) {\n"
                "            Element top = pq.poll();\n"
                "            val = top.val;\n"
                "            if(top.c + 1 < N) pq.add(new Element(matrix[top.r][top.c+1], top.r, top.c+1));\n"
                "        }\n"
                "        System.out.println(val);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "3 8\n1 5 9\n10 11 13\n12 13 15", "output": "13", "explanation": "Sorted matrix elements: [1,5,9,10,11,12,13,13,15]. Rank 8 is 13."}
        ],
        "hiddenTestCases": [
            {"input": "3 8\n1 5 9\n10 11 13\n12 13 15", "output": "13", "isSample": True},
            {"input": "1 1\n5", "output": "5", "isSample": False},
            {"input": "2 2\n1 2\n3 4", "output": "2", "isSample": False},
            {"input": "2 4\n1 2\n3 4", "output": "4", "isSample": False},
            {"input": "3 1\n1 2 3\n4 5 6\n7 8 9", "output": "1", "isSample": False}
        ]
    },
    {
        "id": "house-burglar",
        "title": "House Burglar",
        "difficulty": "Medium",
        "tags": ["Dynamic Programming"],
        "enabled": True,
        "description": (
            "Calculate the maximum money you can rob from houses along a street without robbing adjacent houses.\n\n"
            "Input:\n"
            "A single line containing comma-separated house cash values (e.g. `2,7,9,3,1`).\n\n"
            "Output:\n"
            "Print the maximum robbery sum."
        ),
        "constraints": ["1 <= houses.length <= 10^4", "0 <= cash[i] <= 10^4"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "values = [int(x) for x in sys.stdin.read().strip().split(',')]\n"
                "if not values: print(0)\n"
                "else:\n"
                "    prev1, prev2 = 0, 0\n"
                "    for num in values:\n"
                "        prev1, prev2 = max(prev2 + num, prev1), prev1\n"
                "    print(prev1)\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const vals = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(',').map(Number);\n"
                "if(vals.length === 0) { console.log(0); } else {\n"
                "    let prev1 = 0, prev2 = 0;\n"
                "    for(let val of vals) {\n"
                "        let temp = prev1;\n"
                "        prev1 = Math.max(prev2 + val, prev1);\n"
                "        prev2 = temp;\n"
                "    }\n"
                "    console.log(prev1);\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string line; if(!getline(cin, line)) { cout << 0 << endl; return 0; }\n"
                "    vector<int> nums;\n"
                "    stringstream ss(line);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) nums.push_back(stoi(val));\n"
                "    int prev1 = 0, prev2 = 0;\n"
                "    for (int x : nums) {\n"
                "        int temp = prev1;\n"
                "        prev1 = max(prev2 + x, prev1);\n"
                "        prev2 = temp;\n"
                "    }\n"
                "    cout << prev1 << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNext()) { System.out.println(0); return; }\n"
                "        String[] strs = sc.next().split(\",\");\n"
                "        int prev1 = 0, prev2 = 0;\n"
                "        for(String s : strs) {\n"
                "            int val = Integer.parseInt(s.trim());\n"
                "            int temp = prev1;\n"
                "            prev1 = Math.max(prev2 + val, prev1);\n"
                "            prev2 = temp;\n"
                "        }\n"
                "        System.out.println(prev1);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "2,7,9,3,1", "output": "12", "explanation": "Rob house 1 (2), house 3 (9), house 5 (1). Max is 12."}
        ],
        "hiddenTestCases": [
            {"input": "2,7,9,3,1", "output": "12", "isSample": True},
            {"input": "1,2,3,1", "output": "4", "isSample": False},
            {"input": "0", "output": "0", "isSample": False},
            {"input": "5,1,1,5", "output": "10", "isSample": False},
            {"input": "100,1,1,100", "output": "200", "isSample": False}
        ]
    },
    {
        "id": "edit-distance",
        "title": "Edit Distance",
        "difficulty": "Hard",
        "tags": ["Dynamic Programming", "String"],
        "enabled": True,
        "description": (
            "Find the minimum number of single-character operations (insert, delete, replace) required to convert string $A$ to string $B$.\n\n"
            "Input:\n"
            "Line 1: Word A.\n"
            "Line 2: Word B.\n\n"
            "Output:\n"
            "Print the edit distance integer."
        ),
        "constraints": ["0 <= A.length, B.length <= 500"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "w1 = lines[0] if len(lines) > 0 else ''\n"
                "w2 = lines[1] if len(lines) > 1 else ''\n"
                "m, n = len(w1), len(w2)\n"
                "dp = [[0]*(n+1) for _ in range(m+1)]\n"
                "for i in range(m+1): dp[i][0] = i\n"
                "for j in range(n+1): dp[0][j] = j\n"
                "for i in range(1, m+1):\n"
                "    for j in range(1, n+1):\n"
                "        if w1[i-1] == w2[j-1]: dp[i][j] = dp[i-1][j-1]\n"
                "        else: dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1\n"
                "print(dp[m][n])\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').split('\\n');\n"
                "const w1 = lines[0] ? lines[0].trim() : '';\n"
                "const w2 = lines[1] ? lines[1].trim() : '';\n"
                "const m = w1.length, n = w2.length;\n"
                "const dp = Array.from({length: m+1}, () => Array(n+1).fill(0));\n"
                "for(let i=0; i<=m; i++) dp[i][0] = i;\n"
                "for(let j=0; j<=n; j++) dp[0][j] = j;\n"
                "for(let i=1; i<=m; i++) {\n"
                "    for(let j=1; j<=n; j++) {\n"
                "        if(w1[i-1] === w2[j-1]) dp[i][j] = dp[i-1][j-1];\n"
                "        else dp[i][j] = Math.min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1;\n"
                "    }\n"
                "}\n"
                "console.log(dp[m][n]);\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <string>\n"
                "#include <vector>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string w1, w2;\n"
                "    if(!getline(cin, w1)) w1 = \"\";\n"
                "    if(!getline(cin, w2)) w2 = \"\";\n"
                "    int m = w1.length(), n = w2.length();\n"
                "    vector<vector<int>> dp(m + 1, vector<int>(n + 1));\n"
                "    for(int i = 0; i <= m; i++) dp[i][0] = i;\n"
                "    for(int j = 0; j <= n; j++) dp[0][j] = j;\n"
                "    for(int i = 1; i <= m; i++) {\n"
                "        for(int j = 1; j <= n; j++) {\n"
                "            if(w1[i - 1] == w2[j - 1]) dp[i][j] = dp[i - 1][j - 1];\n"
                "            else dp[i][j] = min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]}) + 1;\n"
                "        }\n"
                "    }\n"
                "    cout << dp[m][n] << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        String w1 = sc.hasNextLine() ? sc.nextLine().trim() : \"\";\n"
                "        String w2 = sc.hasNextLine() ? sc.nextLine().trim() : \"\";\n"
                "        int m = w1.length(), n = w2.length();\n"
                "        int[][] dp = new int[m + 1][n + 1];\n"
                "        for(int i = 0; i <= m; i++) dp[i][0] = i;\n"
                "        for(int j = 0; j <= n; j++) dp[0][j] = j;\n"
                "        for(int i = 1; i <= m; i++) {\n"
                "            for(int j = 1; j <= n; j++) {\n"
                "                if(w1.charAt(i - 1) == w2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];\n"
                "                else dp[i][j] = Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]) + 1;\n"
                "            }\n"
                "        }\n"
                "        System.out.println(dp[m][n]);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "horse\nros", "output": "3", "explanation": "horse -> rorse -> rose -> ros (3 operations)."}
        ],
        "hiddenTestCases": [
            {"input": "horse\nros", "output": "3", "isSample": True},
            {"input": "intention\nexecution", "output": "5", "isSample": False},
            {"input": "\n", "output": "0", "isSample": False},
            {"input": "abc\n", "output": "3", "isSample": False},
            {"input": "abc\nabc", "output": "0", "isSample": False}
        ]
    },
    {
        "id": "subarray-sum-k",
        "title": "Subarray Sum Equals K",
        "difficulty": "Medium",
        "tags": ["Prefix Sum", "Hash Map"],
        "enabled": True,
        "description": (
            "Given an array of integers, count the total number of contiguous subarrays that sum up to $K$.\n\n"
            "Input:\n"
            "Line 1: A comma-separated list of integers.\n"
            "Line 2: The target sum $K$.\n\n"
            "Output:\n"
            "Print the count of contiguous subarrays."
        ),
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-1000 <= nums[i] <= 1000", "-10^7 <= K <= 10^7"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "if lines:\n"
                "    nums = [int(x) for x in lines[0].split(',')]\n"
                "    k = int(lines[1])\n"
                "    prefix_sums = {0: 1}\n"
                "    curr, count = 0, 0\n"
                "    for num in nums:\n"
                "        curr += num\n"
                "        if curr - k in prefix_sums:\n"
                "            count += prefix_sums[curr - k]\n"
                "        prefix_sums[curr] = prefix_sums.get(curr, 0) + 1\n"
                "    print(count)\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if(lines.length >= 2) {\n"
                "    const nums = lines[0].split(',').map(Number);\n"
                "    const k = Number(lines[1]);\n"
                "    const prefix = {0: 1};\n"
                "    let curr = 0, count = 0;\n"
                "    for(let val of nums) {\n"
                "        curr += val;\n"
                "        if((curr - k) in prefix) count += prefix[curr - k];\n"
                "        prefix[curr] = (prefix[curr] || 0) + 1;\n"
                "    }\n"
                "    console.log(count);\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "#include <unordered_map>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string l1, l2; if(!getline(cin, l1)) return 0;\n"
                "    getline(cin, l2); int k = stoi(l2);\n"
                "    vector<int> nums;\n"
                "    stringstream ss(l1);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) nums.push_back(stoi(val));\n"
                "    unordered_map<int, int> prefix;\n"
                "    prefix[0] = 1;\n"
                "    int curr = 0, count = 0;\n"
                "    for(int x : nums) {\n"
                "        curr += x;\n"
                "        if(prefix.count(curr - k)) count += prefix[curr - k];\n"
                "        prefix[curr]++;\n"
                "    }\n"
                "    cout << count << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextLine()) return;\n"
                "        String[] strs = sc.nextLine().split(\",\");\n"
                "        int k = sc.nextInt();\n"
                "        Map<Integer, Integer> prefix = new HashMap<>();\n"
                "        prefix.put(0, 1);\n"
                "        int curr = 0, count = 0;\n"
                "        for(String s : strs) {\n"
                "            curr += Integer.parseInt(s.trim());\n"
                "            if(prefix.containsKey(curr - k)) count += prefix.get(curr - k);\n"
                "            prefix.put(curr, prefix.getOrDefault(curr, 0) + 1);\n"
                "        }\n"
                "        System.out.println(count);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "1,1,1\n2", "output": "2", "explanation": "[1,1] at index 0..1 and index 1..2 both sum to 2."}
        ],
        "hiddenTestCases": [
            {"input": "1,1,1\n2", "output": "2", "isSample": True},
            {"input": "1,2,3\n3", "output": "2", "isSample": False},
            {"input": "1\n0", "output": "0", "isSample": False},
            {"input": "-1,-1,1\n0", "output": "1", "isSample": False},
            {"input": "0,0,0,0\n0", "output": "10", "isSample": False}
        ]
    },
    {
        "id": "max-subarray-product",
        "title": "Max Subarray Product",
        "difficulty": "Medium",
        "tags": ["Dynamic Programming", "Array"],
        "enabled": True,
        "description": (
            "Given an integer array, find the contiguous subarray that has the largest product.\n\n"
            "Input:\n"
            "A single line of comma-separated integers.\n"
            "Output:\n"
            "Print the maximum product integer."
        ),
        "constraints": ["1 <= nums.length <= 2 * 10^4", "-10 <= nums[i] <= 10"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "vals = [int(x) for x in sys.stdin.read().strip().split(',')]\n"
                "if not vals: print(0)\n"
                "else:\n"
                "    res = max_p = min_p = vals[0]\n"
                "    for x in vals[1:]:\n"
                "        choices = (x, max_p * x, min_p * x)\n"
                "        max_p = max(choices)\n"
                "        min_p = min(choices)\n"
                "        res = max(res, max_p)\n"
                "    print(res)\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const vals = fs.readFileSync('/dev/stdin', 'utf-8').trim().split(',').map(Number);\n"
                "if(vals.length === 0) { console.log(0); } else {\n"
                "    let res = vals[0], max_p = vals[0], min_p = vals[0];\n"
                "    for(let i=1; i<vals.length; i++) {\n"
                "        let x = vals[i];\n"
                "        let choices = [x, max_p * x, min_p * x];\n"
                "        max_p = Math.max(...choices);\n"
                "        min_p = Math.min(...choices);\n"
                "        res = Math.max(res, max_p);\n"
                "    }\n"
                "    console.log(res);\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string line; if(!getline(cin, line)) { cout << 0 << endl; return 0; }\n"
                "    vector<int> nums;\n"
                "    stringstream ss(line);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) nums.push_back(stoi(val));\n"
                "    int res = nums[0], max_p = nums[0], min_p = nums[0];\n"
                "    for(size_t i = 1; i < nums.size(); i++) {\n"
                "        int x = nums[i];\n"
                "        int temp = max_p;\n"
                "        max_p = max({x, max_p * x, min_p * x});\n"
                "        min_p = min({x, temp * x, min_p * x});\n"
                "        res = max(res, max_p);\n"
                "    }\n"
                "    cout << res << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNext()) { System.out.println(0); return; }\n"
                "        String[] strs = sc.next().split(\",\");\n"
                "        int[] nums = new int[strs.length];\n"
                "        for (int i = 0; i < strs.length; i++) nums[i] = Integer.parseInt(strs[i].trim());\n"
                "        int res = nums[0], max_p = nums[0], min_p = nums[0];\n"
                "        for(int i = 1; i < nums.length; i++) {\n"
                "            int x = nums[i];\n"
                "            int temp = max_p;\n"
                "            max_p = Math.max(x, Math.max(max_p * x, min_p * x));\n"
                "            min_p = Math.min(x, Math.min(temp * x, min_p * x));\n"
                "            res = Math.max(res, max_p);\n"
                "        }\n"
                "        System.out.println(res);\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "2,3,-2,4", "output": "6", "explanation": "[2,3] yields the max product 6."}
        ],
        "hiddenTestCases": [
            {"input": "2,3,-2,4", "output": "6", "isSample": True},
            {"input": "-2,0,-1", "output": "0", "isSample": False},
            {"input": "-3,-4,-5", "output": "20", "isSample": False},
            {"input": "5", "output": "5", "isSample": False},
            {"input": "-2,3,-4", "output": "24", "isSample": False}
        ]
    },
    {
        "id": "n-queens",
        "title": "N-Queens Puzzle",
        "difficulty": "Hard",
        "tags": ["Backtracking"],
        "enabled": True,
        "description": (
            "Find the number of distinct solutions to place $N$ queens on an $N \\times N$ chessboard such that no two queens attack each other.\n\n"
            "Input:\n"
            "A single integer representing the board size $N$.\n\n"
            "Output:\n"
            "Print the integer representing total solutions."
        ),
        "constraints": ["1 <= N <= 12"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "N = int(sys.stdin.read().strip())\n"
                "def solve(r, cols, diag1, diag2):\n"
                "    if r == N: return 1\n"
                "    count = 0\n"
                "    for c in range(N):\n"
                "        d1, d2 = r - c, r + c\n"
                "        if c not in cols and d1 not in diag1 and d2 not in diag2:\n"
                "            cols.add(c); diag1.add(d1); diag2.add(d2)\n"
                "            count += solve(r+1, cols, diag1, diag2)\n"
                "            cols.remove(c); diag1.remove(d1); diag2.remove(d2)\n"
                "    return count\n"
                "print(solve(0, set(), set(), set()))\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const N = Number(fs.readFileSync('/dev/stdin', 'utf-8').trim());\n"
                "const cols = new Set(), d1 = new Set(), d2 = new Set();\n"
                "function solve(r) {\n"
                "    if(r === N) return 1;\n"
                "    let count = 0;\n"
                "    for(let c=0; c<N; c++) {\n"
                "        if(!cols.has(c) && !d1.has(r-c) && !d2.has(r+c)) {\n"
                "            cols.add(c); d1.add(r-c); d2.add(r+c);\n"
                "            count += solve(r+1);\n"
                "            cols.delete(c); d1.delete(r-c); d2.delete(r+c);\n"
                "        }\n"
                "    }\n"
                "    return count;\n"
                "}\n"
                "console.log(solve(0));\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <set>\n"
                "using namespace std;\n"
                "int N;\n"
                "int solve(int r, set<int>& cols, set<int>& d1, set<int>& d2) {\n"
                "    if (r == N) return 1;\n"
                "    int count = 0;\n"
                "    for (int c = 0; c < N; c++) {\n"
                "        if (!cols.count(c) && !d1.count(r - c) && !d2.count(r + c)) {\n"
                "            cols.insert(c); d1.insert(r - c); d2.insert(r + c);\n"
                "            count += solve(r + 1, cols, d1, d2);\n"
                "            cols.erase(c); d1.erase(r - c); d2.erase(r + c);\n"
                "        }\n"
                "    }\n"
                "    return count;\n"
                "}\n"
                "int main() {\n"
                "    if (!(cin >> N)) return 0;\n"
                "    set<int> cols, d1, d2;\n"
                "    cout << solve(0, cols, d1, d2) << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    static int N;\n"
                "    static Set<Integer> cols = new HashSet<>();\n"
                "    static Set<Integer> d1 = new HashSet<>();\n"
                "    static Set<Integer> d2 = new HashSet<>();\n"
                "    static int solve(int r) {\n"
                "        if(r == N) return 1;\n"
                "        int count = 0;\n"
                "        for(int c=0; c<N; c++) {\n"
                "            if(!cols.contains(c) && !d1.contains(r-c) && !d2.contains(r+c)) {\n"
                "                cols.add(c); d1.add(r-c); d2.add(r+c);\n"
                "                count += solve(r+1);\n"
                "                cols.remove(c); d1.remove(r-c); d2.remove(r+c);\n"
                "            }\n"
                "        }\n"
                "        return count;\n"
                "    }\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextInt()) return;\n"
                "        N = sc.nextInt();\n"
                "        System.out.println(solve(0));\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "4", "output": "2", "explanation": "2 safe placement solutions on a 4x4 board."}
        ],
        "hiddenTestCases": [
            {"input": "4", "output": "2", "isSample": True},
            {"input": "1", "output": "1", "isSample": False},
            {"input": "2", "output": "0", "isSample": False},
            {"input": "8", "output": "92", "isSample": False},
            {"input": "5", "output": "10", "isSample": False}
        ]
    },
    {
        "id": "task-scheduling",
        "title": "Task Scheduling",
        "difficulty": "Medium",
        "tags": ["Greedy", "Hash Map"],
        "enabled": True,
        "description": (
            "Calculate the least CPU intervals needed to finish a list of tasks. "
            "Tasks are represented by character lists (A to Z). "
            "There is a cooling period $N$ between identical tasks where CPU must remain idle.\n\n"
            "Input:\n"
            "Line 1: Comma-separated characters (e.g. `A,A,A,B,B,B`).\n"
            "Line 2: Cooling integer $N$.\n\n"
            "Output:\n"
            "Print the minimum intervals count."
        ),
        "constraints": ["1 <= tasks.length <= 10^4", "0 <= N <= 100"],
        "starterTemplates": {
            "python": (
                "import sys\n"
                "lines = sys.stdin.read().splitlines()\n"
                "if lines:\n"
                "    tasks = lines[0].split(',')\n"
                "    n = int(lines[1])\n"
                "    freqs = {}\n"
                "    for t in tasks: freqs[t] = freqs.get(t, 0) + 1\n"
                "    max_val = max(freqs.values())\n"
                "    max_count = list(freqs.values()).count(max_val)\n"
                "    ans = (max_val - 1) * (n + 1) + max_count\n"
                "    print(max(ans, len(tasks)))\n"
            ),
            "javascript": (
                "const fs = require('fs');\n"
                "const lines = fs.readFileSync('/dev/stdin', 'utf-8').trim().split('\\n');\n"
                "if(lines.length >= 2) {\n"
                "    const tasks = lines[0].split(',');\n"
                "    const n = Number(lines[1]);\n"
                "    const freqs = {};\n"
                "    for(let t of tasks) freqs[t] = (freqs[t] || 0) + 1;\n"
                "    const vals = Object.values(freqs);\n"
                "    const maxVal = Math.max(...vals);\n"
                "    const maxCount = vals.filter(v => v === maxVal).length;\n"
                "    const ans = (maxVal - 1) * (n + 1) + maxCount;\n"
                "    console.log(Math.max(ans, tasks.length));\n"
                "}\n"
            ),
            "cpp": (
                "#include <iostream>\n"
                "#include <vector>\n"
                "#include <unordered_map>\n"
                "#include <string>\n"
                "#include <sstream>\n"
                "#include <algorithm>\n"
                "using namespace std;\n"
                "int main() {\n"
                "    string l1, l2; if(!getline(cin, l1)) return 0;\n"
                "    getline(cin, l2); int n = stoi(l2);\n"
                "    vector<string> tasks;\n"
                "    stringstream ss(l1);\n"
                "    string val;\n"
                "    while(getline(ss, val, ',')) tasks.push_back(val);\n"
                "    unordered_map<string, int> freqs;\n"
                "    for(auto& t : tasks) freqs[t]++;\n"
                "    int maxVal = 0;\n"
                "    for(auto& pair : freqs) maxVal = max(maxVal, pair.second);\n"
                "    int maxCount = 0;\n"
                "    for(auto& pair : freqs) {\n"
                "        if(pair.second == maxVal) maxCount++;\n"
                "    }\n"
                "    int ans = (maxVal - 1) * (n + 1) + maxCount;\n"
                "    cout << max(ans, (int)tasks.size()) << endl;\n"
                "    return 0;\n"
                "}\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        if(!sc.hasNextLine()) return;\n"
                "        String[] tasks = sc.nextLine().split(\",\");\n"
                "        int n = sc.nextInt();\n"
                "        Map<String, Integer> freqs = new HashMap<>();\n"
                "        for(String t : tasks) {\n"
                "            String key = t.trim();\n"
                "            freqs.put(key, freqs.getOrDefault(key, 0) + 1);\n"
                "        }\n"
                "        int maxVal = 0;\n"
                "        for(int val : freqs.values()) maxVal = Math.max(maxVal, val);\n"
                "        int maxCount = 0;\n"
                "        for(int val : freqs.values()) {\n"
                "            if(val == maxVal) maxCount++;\n"
                "        }\n"
                "        int ans = (maxVal - 1) * (n + 1) + maxCount;\n"
                "        System.out.println(Math.max(ans, tasks.length));\n"
                "    }\n"
                "}\n"
            )
        },
        "sampleCases": [
            {"input": "A,A,A,B,B,B\n2", "output": "8", "explanation": "A -> B -> idle -> A -> B -> idle -> A -> B."}
        ],
        "hiddenTestCases": [
            {"input": "A,A,A,B,B,B\n2", "output": "8", "isSample": True},
            {"input": "A,A,A,B,B,B\n0", "output": "6", "isSample": False},
            {"input": "A\n3", "output": "1", "isSample": False},
            {"input": "A,B,C,D,E,F\n3", "output": "6", "isSample": False},
            {"input": "A,A,A,A,B,C,D\n2", "output": "10", "isSample": False}
        ]
    }
]

def seed_db():
    print("Beginning seeding process...")
    for p in problems:
        p_id = p["id"]
        # Extract and remove hiddenTestCases from top-level problem payload
        tcs = p.pop("hiddenTestCases", [])
        
        # Add timestamp metadata
        p["createdAt"] = firestore.SERVER_TIMESTAMP
        p["updatedAt"] = firestore.SERVER_TIMESTAMP
        
        # Set problem document
        p_ref = db.collection('problems').document(p_id)
        p_ref.set(p)
        print(f"Seeded problem metadata: '{p_id}'")
        
        # Write subcollection hiddenTestCases
        tcs_ref = p_ref.collection('hiddenTestCases')
        for i, tc in enumerate(tcs):
            tc_id = f"tc_{i+1}"
            tcs_ref.document(tc_id).set({
                "input": tc["input"],
                "output": tc["output"],
                "isSample": tc.get("isSample", False)
            })
        print(f"  - Seeded {len(tcs)} hidden test cases for '{p_id}'")
    print("Database seeding completed successfully.")

if __name__ == '__main__':
    seed_db()
