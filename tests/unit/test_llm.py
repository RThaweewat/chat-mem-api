from src.services.llm import handle_chat


def test_handle_chat():
    """
    Tests the `handle_chat` function with a query that requests a simple
    mathematical operation (addition) and verifies that the result is returned
    correctly as a single-digit number. The test follows an assertion pattern
    to compare the expected result with the actual output.

    :return: This function does not return a value. It asserts the correctness
             of the function it tests.
    """
    query = "What is 1+2?, return number only, no other text, 1 digit long"
    expected_result = "3"
    result = handle_chat(query)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"
