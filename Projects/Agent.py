import os
import re
import openai  # pip install openai

# 1. SETUP - Replace with your actual API key
client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY")

# 2. DEFINE TOOLS (The "Arms" of the Agent)
def get_weather(location):
    """Simulated weather API."""
    data = {"london": "15°C, Rainy", "new york": "22°C, Sunny", "tokyo": "18°C, Windy"}
    return data.get(location.lower(), "Weather data not found for this location.")

def calculator(expression):
    """Safely evaluates math."""
    try:
        # Note: In production, use a safer math parser than eval()
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

# Mapping tool names to functions
available_tools = {
    "get_weather": get_weather,
    "calculator": calculator
}

# 3. THE BRAIN (System Prompt)
SYSTEM_PROMPT = """
You are a helpful AI Agent that solves problems using tools. 
You must follow this exact cycle:

Thought: [Your reasoning about what to do next]
Action: tool_name("input_string")
Observation: [The result of the tool - this will be provided to you]

... (Repeat Thought/Action/Observation if needed)

Final Answer: [Your final response to the user]

Available Tools:
- get_weather(location): Returns weather for a city. Input must be a string.
- calculator(expression): Solves math. Input must be a math string like "5 * 5".
"""

# 4. THE AGENT LOOP
def run_agent(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    print(f"\n🚀 Task: {user_input}\n" + "="*30)

    for i in range(5):  # Max iterations to prevent infinite loops
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0 # Keep it deterministic
        ).choices[0].message.content

        print(f"\n{response}")

        if "Final Answer:" in response:
            return response

        # REGEX to find Action: tool_name("args")
        action_match = re.search(r"Action:\s*(\w+)\((.*)\)", response)
        
        if action_match:
            tool_name = action_match.group(1)
            # Clean up arguments (remove quotes)
            tool_input = action_match.group(2).strip().strip('"').strip("'")
            
            if tool_name in available_tools:
                print(f"🔧 Running tool: {tool_name} with input: {tool_input}")
                observation = available_tools[tool_name](tool_input)
                
                # Update history with the thought and the observation
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                messages.append({"role": "user", "content": f"Observation: Tool {tool_name} not found."})
        else:
            # If the LLM didn't format the action correctly
            break

    return "Agent failed to find an answer within the step limit."

# 5. EXECUTION
if __name__ == "__main__":
    query = "What is the weather in London and what is that temperature in Fahrenheit if we multiply it by 1.8 and add 32?"
    run_agent(query)