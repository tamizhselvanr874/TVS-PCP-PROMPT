import streamlit as st  
import openai  
  
# Configure Azure OpenAI API  
openai.api_key = "783973291a7c4a74a1120133309860c0"  
openai.api_base = "https://theswedes.openai.azure.com/"  
openai.api_type = "azure"  
openai.api_version = "2024-05-01-preview"  
deployment_name = "GPT-4-Omni"  
  
def generate_response(prompt):  
    try:  
        response = openai.ChatCompletion.create(  
            engine=deployment_name,  
            messages=[  
                {"role": "system", "content": "You are an assistant."},  
                {"role": "user", "content": prompt}  
            ],  
            max_tokens=3000,  
            temperature=0.3  
        )  
        return response.choices[0].message['content'].strip()  
    except Exception as e:  
        st.error(f"An error occurred: {e}")  
        return None  
  
def pcp_prompt(user_query):  
    # Initial prompt using PCP framework  
    initial_prompt = f"Objective: Analyze the user's query comprehensively. User query: {user_query}"  
    response1 = generate_response(initial_prompt)  
  
    # Follow-up prompt with cumulative context embedding  
    follow_up_prompt = (f"In our earlier discussion, we focused on understanding: {user_query}. "  
                        f"To further refine these insights, please expand on the detailed analysis of the topic.")  
    response2 = generate_response(follow_up_prompt)  
  
    # Next follow-up prompt  
    next_follow_up_prompt = (f"Based on the detailed analysis provided, what additional insights can be gained "  
                             f"to enhance understanding of the user's query: {user_query}?")  
    response3 = generate_response(next_follow_up_prompt)  
  
    return response1, response2, response3  
  
def main():  
    st.title("TVS's PCP Technique")  
    user_query = st.text_input("Enter your query:")  
  
    if user_query:  
        # Short response  
        short_response_prompt = f"Please provide a short answer to the following query: {user_query}"  
        short_response = generate_response(short_response_prompt)  
  
        # Detailed response using PCP  
        response1, response2, response3 = pcp_prompt(user_query)  
        detailed_response = f"{response1}\n{response2}\n{response3}"  
  
        # Display results in a table  
        st.subheader("Results")  
        results = {  
            "Method": ["Short Response", "PCP Technique"],  
            "Response": [short_response, detailed_response]  
        }  
        st.table(results)  
  
        # Evaluation  
        # st.subheader("Evaluation")  
        # st.write("The PCP technique is superior because it provides a comprehensive understanding by utilizing "  
        #          "progressive contextual embedding and follow-up prompts that retain context and build upon previous "  
        #          "insights. This approach ensures that the responses are detailed and aligned with the user's objective.")  
        # st.write("Suggestion: The PCP technique is recommended for obtaining a detailed and insightful response.")  
  
if __name__ == '__main__':  
    main()  