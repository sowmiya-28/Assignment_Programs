#include <iostream>
#include <string>
#include <cassert>
using namespace std;

string reverse_words(const string& str) {
    string result = str;
    int i = 0;

    while (i < result.size()) {

        if (!isalnum(result[i])) {
            i++;
            continue;
        }

        int start = i;
        while (i < result.size() && isalnum(result[i])) {
            i++;
        }
        int end = i - 1;

        while (start < end) {
            swap(result[start], result[end]);
            start++;
            end--;
        }
    }

    return result;
}

int main() {
    string test_str = "String; 2be reversed...";
    assert(reverse_words(test_str) == "gnirtS; eb2 desrever...");
    cout << "Test 1 passed: " << reverse_words(test_str) << endl;

    return 0;
}