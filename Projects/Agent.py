import os
import re
import openai

# 1. SECURE SETUP
# This line now looks for the 'OPENAI_API_KEY' you set in your terminal
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or "YOUR_OPE" in api_key:
    print("❌ Error: API Key not found or still set to placeholder.")
    print("Please run: $env:OPENAI_API_KEY='your-actual-key-here'")
    exit()

client = openai.OpenAI(api_key=api_key)

# 2. DEFINE TOOLS
def get_weather(location):
    """Simulated weather API."""
    data = {"london": "15", "new york": "22", "tokyo": "18"}
    return data.get(location.lower(), "20") # Default to 20 if city not found

def calculator(expression):
    """Safely evaluates math."""
    try:
        # Simple regex to allow only numbers and basic operators for safety
        clean_expr = re.sub(r'[^0-9\+\-\*\/\.\(\) ]', '', expression)
        return str(eval(clean_expr))
    except Exception as e:
        return f"Error: {str(e)}"

available_tools = {
    "get_weather": get_weather,
    "calculator": calculator
}

# 3. THE SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a ReAct AI Agent. You solve tasks by thinking and acting.
Available Tools:
- get_weather(location): Returns temperature in Celsius as a number.
- calculator(expression): Solves math problems.

Format:
Thought: <reasoning>
Action: <tool_name>(<input>)
Observation: <result from tool>
... (repeat)
Final Answer: <the ultimate response>
"""

# 4. THE AGENT LOOP
def run_agent(user_input):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    print(f"\n🚀 Task: {user_input}\n" + "="*40)

    for i in range(5):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0
        ).choices[0].message.content

        print(f"\n{response}")

        if "Final Answer:" in response:
            return response

        # Robust Regex to extract Action: tool_name("input") or tool_name(input)
        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", response)
        
        if action_match:
            tool_name = action_match.group(1)
            tool_input = action_match.group(2).strip().strip('"').strip("'")
            
            if tool_name in available_tools:
                print(f"🔧 [System]: Executing {tool_name}...")
                observation = available_tools[tool_name](tool_input)
                
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                messages.append({"role": "user", "content": f"Error: Tool {tool_name} does not exist."})
        else:
            break

# 5. EXECUTION
if __name__ == "__main__":
    query = "What is the weather in London and what is that temperature in Fahrenheit if we multiply it by 1.8 and add 32?"
    run_agent(query)