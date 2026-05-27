import os
from typing import Optional
import json

from google import genai
from google.genai import types

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


class Agent:
    """Agent individual que ejecuta tareas específicas"""

    def __init__(self, name: str, role: str, instructions: str):
        self.name = name
        self.role = role
        self.instructions = instructions
        self._client = None

    def _get_client(self):
        """Crea el cliente de Gemini de forma perezosa (solo al usarse)."""
        if self._client is None:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "Falta la API key de Gemini. Define GEMINI_API_KEY en el archivo .env"
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def execute(self, task: str, context: dict = None) -> dict:
        """Ejecutar tarea del agent"""
        context_str = json.dumps(context) if context else ""

        prompt = f"""
        You are {self.name}, a {self.role}.

        Instructions: {self.instructions}

        Context: {context_str}

        Task: {task}

        Provide a structured response with:
        1. Analysis
        2. Recommendations
        3. Next steps
        """

        response = self._get_client().models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=1024),
        )

        return {
            'agent': self.name,
            'response': response.text,
            'status': 'completed'
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
            instructions="""
            You are specialized in searching and filtering real estate properties.
            Analyze user requirements and search criteria.
            Extract key parameters: location, price range, property type, amenities.
            Provide structured search recommendations.
            """
        )
        
        # Agent 2: Evaluador de Propiedades
        self.agents['evaluator'] = Agent(
            name="PropertyEvaluator",
            role="Real Estate Valuation Expert",
            instructions="""
            You are specialized in property evaluation and valuation.
            Analyze property details, market comparables, and location factors.
            Provide investment potential assessment.
            Give price recommendations and market analysis.
            """
        )
        
        # Agent 3: Asesor Financiero
        self.agents['finance'] = Agent(
            name="FinancialAdvisor",
            role="Mortgage and Financial Planning Expert",
            instructions="""
            You are specialized in mortgage calculations and financial planning.
            Provide mortgage estimates, down payment recommendations.
            Analyze affordability based on income and property price.
            Suggest financing options and payment plans.
            """
        )
        
        # Agent 4: Especialista Legal
        self.agents['legal'] = Agent(
            name="LegalAdvisor",
            role="Real Estate Legal Expert",
            instructions="""
            You are specialized in real estate legal matters.
            Provide information about property documentation requirements.
            Explain legal considerations, contracts, and regulations.
            Give advice on due diligence and documentation.
            """
        )
        
        # Agent 5: Coordinador
        self.agents['coordinator'] = Agent(
            name="Coordinator",
            role="Real Estate Transaction Coordinator",
            instructions="""
            You are specialized in coordinating real estate transactions.
            Orchestrate workflow between different specialists.
            Synthesize recommendations from all agents.
            Provide comprehensive transaction guidance.
            """
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
