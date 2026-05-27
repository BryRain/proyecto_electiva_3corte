import requests
from typing import Optional
import json
import os

class Agent:
    """Agent individual que ejecuta tareas específicas"""
    
    def __init__(self, name: str, role: str, instructions: str):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY no está configurada")
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openai/gpt-3.5-turbo"  # O puedes usar otro modelo disponible
    
    def execute(self, task: str, context: dict = None) -> dict:
        """Ejecutar tarea del agent"""
        context_str = json.dumps(context) if context else ""
        
        prompt = f"""You are {self.name}, a {self.role}.

Instructions: {self.instructions}

Context: {context_str}

Task: {task}

Provide a structured response with:
1. Analysis
2. Recommendations
3. Next steps"""
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": f"You are {self.name}, a {self.role}. {self.instructions}"},
                        {"role": "user", "content": task}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Error en OpenRouter: {response.text}")
            
            data = response.json()
            response_text = data['choices'][0]['message']['content']
            
            return {
                'agent': self.name,
                'response': response_text,
                'status': 'completed'
            }
        except Exception as e:
            return {
                'agent': self.name,
                'response': f'Error: {str(e)}',
                'status': 'error'
            }

class MultiAgent:
    """Sistema Multi-Agent coordinado"""
    
    def __init__(self):
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Inicializar los agentes del sistema"""
        
        # Agent 1: Buscador de Propiedades
        self.agents['search'] = Agent(
            name="SearchAgent",
            role="Real Estate Property Search Specialist",
            instructions="Search for properties based on user criteria. Return only key search parameters and 2-3 recommendations in 100 words max."
        )
        
        # Agent 2: Evaluador de Propiedades
        self.agents['evaluator'] = Agent(
            name="PropertyEvaluator",
            role="Real Estate Valuation Expert",
            instructions="Evaluate properties and market. Provide brief assessment in 80 words max. Focus on: price fairness, location, investment potential."
        )
        
        # Agent 3: Asesor Financiero
        self.agents['finance'] = Agent(
            name="FinancialAdvisor",
            role="Mortgage and Financial Planning Expert",
            instructions="Provide mortgage estimates. Be brief: estimate down payment and monthly payment in 80 words max. Ask only essential questions."
        )
        
        # Agent 4: Especialista Legal
        self.agents['legal'] = Agent(
            name="LegalAdvisor",
            role="Real Estate Legal Expert",
            instructions="Provide legal considerations for property purchase. Keep it brief (60 words): title, documents needed, due diligence checklist."
        )
        
        # Agent 5: Coordinador
        self.agents['coordinator'] = Agent(
            name="Coordinator",
            role="Real Estate Transaction Coordinator",
            instructions="Synthesize all specialist recommendations into a brief, actionable summary for the client. Maximum 150 words. Focus on: next steps and key recommendations."
        )
    
    def execute_workflow(self, user_query: str, user_context: dict = None) -> dict:
        """Ejecutar flujo completo de IA con múltiples agentes"""
        
        results = {
            'query': user_query,
            'agents_responses': {},
            'synthesis': None,
            'workflow_status': 'completed'
        }
        
        # Fase 1: Búsqueda
        search_result = self.agents['search'].execute(user_query, user_context)
        results['agents_responses']['search'] = search_result
        
        # Fase 2: Evaluación
        evaluator_context = {
            'search_results': search_result['response'],
            'original_query': user_query
        }
        evaluator_result = self.agents['evaluator'].execute(
            "Evaluate the properties found based on the search results.",
            evaluator_context
        )
        results['agents_responses']['evaluator'] = evaluator_result
        
        # Fase 3: Análisis Financiero
        finance_context = {
            'property_evaluation': evaluator_result['response'],
            'user_budget': user_context.get('budget', {}) if user_context else {}
        }
        finance_result = self.agents['finance'].execute(
            "Provide financial analysis and mortgage recommendations.",
            finance_context
        )
        results['agents_responses']['finance'] = finance_result
        
        # Fase 4: Consideraciones Legales
        legal_result = self.agents['legal'].execute(
            "Provide legal advice and documentation requirements for this transaction.",
            {'user_query': user_query}
        )
        results['agents_responses']['legal'] = legal_result
        
        # Fase 5: Síntesis del Coordinador
        synthesis_context = {
            'search': search_result['response'],
            'evaluation': evaluator_result['response'],
            'finance': finance_result['response'],
            'legal': legal_result['response']
        }
        synthesis = self.agents['coordinator'].execute(
            "Synthesize all recommendations into a comprehensive real estate guidance.",
            synthesis_context
        )
        results['synthesis'] = synthesis['response']
        
        return results
    
    def execute_agent(self, agent_name: str, task: str, context: dict = None) -> dict:
        """Ejecutar un agent específico"""
        if agent_name not in self.agents:
            return {'error': f'Agent {agent_name} not found'}
        
        return self.agents[agent_name].execute(task, context)
    
    def get_agents_info(self) -> list:
        """Obtener información de los agentes disponibles"""
        return [
            {
                'name': agent.name,
                'role': agent.role
            }
            for agent in self.agents.values()
        ]
