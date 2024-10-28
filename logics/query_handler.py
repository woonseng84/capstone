import json
from helper_functions import llm

#category_n_course_name = {'National Institute of Education (NIE)':['Arts (with Education)','Science (with Education)'],
#                          'College of Sciences':['Mathematical Sciences','Mathematics & Economics', 'Physics / Applied Physics']}

category_n_course_name = './data/survey2.json'

# Load the JSON file
filepath = './data/survey2.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_courses = json.loads(json_string)


def identify_category_and_courses(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be enclosed in
    the pair of {delimiter}.

    Decide if the query is relevant to any specific degree
    in the list below.

    If there are any relevant degree found, output everything about the degree.

    {category_n_course_name}

    If no relevant degree are found, output an empty list.

    Ensure your response contains only the list degree or an empty list, 
    without any enclosing tags or delimiters.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    category_and_product_response_str = llm.get_completion_by_messages(messages)
    category_and_product_response_str = category_and_product_response_str.replace("'", "\"")
    category_and_product_response = json.loads(category_and_product_response_str)
    return category_and_product_response
    

def get_course_details(list_of_relevant_category_n_course: list[dict]):
    course_names_list = []
    for x in list_of_relevant_category_n_course:
        course_names_list.append(x.get('degree')) # x["course_name"]
        

    list_of_course_details = []
    for course_name in course_names_list:
        print(f"coursename99: ", course_name)
        list_of_course_details.append(course_name)
        print(f"list of courses99: ", list_of_course_details)
        
    return list_of_course_details


def generate_response_based_on_course_details(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    Follow these steps to answer the customer queries.
    The customer query will be delimited with a pair {delimiter}.

    Step 1:{delimiter} If the user is asking about course or dregree, \
    understand the relevant course(s) or degree from the following list.
    All available degree shown in the json data below:
    {product_details}

    Step 2:{delimiter} Use the information about the degree to \
    generate the answer for the customer's query.
    You must only rely on the facts or information in the degree information.
    Your response should be as detail as possible and \
    include information that is useful for customer to better understand the course.

    Step 3:{delimiter}: Answer the customer in a friendly tone.
    Make sure the statements are factually accurate.
    Your response should be comprehensive and informative to help the \
    the customers to make their decision.
    Complete with details such which university and school is or are offering this degree. What is the gross monthly mean \
    and what is the employment rate overall?
    Use Neural Linguistic Programming to construct your response.

    Use the following format:
    Step 1:{delimiter} <step 1 reasoning>
    Step 2:{delimiter} <step 2 reasoning>
    Step 3:{delimiter} <step 3 response to customer>

    Make sure to include {delimiter} to separate every step.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer


def process_user_message(user_input):
    delimiter = "```"

    # Process 1: If Courses are found, look them up
    category_n_course_name = identify_category_and_courses(user_input)
    print("category_n_course_name : ", category_n_course_name)

    # Process 2: Get the Course Details
    course_details = get_course_details(category_n_course_name)
    print("course detail11: ", course_details)

    # Process 3: Generate Response based on Course Details
    reply = generate_response_based_on_course_details(user_input, course_details)

    # Process 4: Append the response to the list of all messages
    return reply
