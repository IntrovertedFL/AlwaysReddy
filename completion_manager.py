from config_loader import config
import re

class CompletionManager:
    def __init__(self, verbose=False, completions_api=config.COMPLETIONS_API):
        """Initialize the CompletionManager with the TTS client."""
        self.client = None
        self.model = None
        self.verbose = verbose
        self._setup_client(completions_api)

    def _setup_client(self, completions_api):
        """Instantiates the appropriate AI client based on configuration file."""
        if completions_api == "openai":
            from llm_apis.openai_client import OpenAIClient
            self.client = OpenAIClient(verbose=self.verbose)
            
        elif completions_api == "together":
            from llm_apis.togetherai_client import TogetherAIClient
            self.client = TogetherAIClient(verbose=self.verbose)

        elif completions_api == "anthropic":
            from llm_apis.anthropic_client import AnthropicClient
            self.client = AnthropicClient(verbose=self.verbose)

        elif completions_api == "perplexity":
            from llm_apis.perplexity_client import PerplexityClient
            self.client = PerplexityClient(verbose=self.verbose)

        elif completions_api == "openrouter":
            from llm_apis.openrouter_client import OpenRouterClient
            self.client = OpenRouterClient(verbose=self.verbose)
        
        elif completions_api == "groq":
            from llm_apis.groq_client import GroqClient
            self.client = GroqClient(verbose=self.verbose)

        elif completions_api == "tabbyapi":
            from llm_apis.tabbyapi_client import TabbyApiClient
            self.client = TabbyApiClient(verbose=self.verbose)

        elif completions_api == "google":
            from llm_apis.gemini_client import GeminiClient
            self.client = GeminiClient(verbose=self.verbose)

        elif completions_api == "portkey":
            from llm_apis.portkey_client import PortkeyClient
            self.client = PortkeyClient(verbose=self.verbose)
        
        elif completions_api == "portkey_prompt":
            from llm_apis.portkey_prompt_client import PortkeyPromptClient
            self.client = PortkeyPromptClient(verbose=self.verbose) 
        
        elif completions_api == "lm_studio":
            from llm_apis.lm_studio_client import LM_StudioClient
            if hasattr(config, 'LM_STUDIO_API_BASE_URL'):
                self.client = LM_StudioClient(base_url=config.LM_STUDIO_API_BASE_URL, verbose=self.verbose)
            else:
                print("No LM_STUDIO_API_BASE_URL found in config.py, using default")
                self.client = LM_StudioClient(verbose=self.verbose)

        elif completions_api == "ollama":
            from llm_apis.ollama_client import OllamaClient
            if hasattr(config, 'OLLAMA_API_BASE_URL'):
                self.client = OllamaClient(base_url=config.OLLAMA_API_BASE_URL, verbose=self.verbose)
                
            else:
                print("No OLLAMA_API_BASE_URL found in config.py, using default")
                self.client = OllamaClient(verbose=self.verbose)
        else:
            raise ValueError("Unsupported completion API service configured")
    
    def get_completion(self, messages, model, **kwargs):
        """Get completion from the selected AI client and return the entire response.

        Args:
            messages (list): List of messages.
            model (str): Model for completion.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The complete response from the AI client, or None if an error occurs.
        """
        try:           
            completion_stream = self.client.stream_completion(messages, model, **kwargs)
            
            # Accumulate the entire response
            full_response = ""
            for chunk in completion_stream:
                full_response += chunk

            return full_response

        except Exception as e:
            if self.verbose:
                import traceback
                traceback.print_exc()
            else:
                print(f"An error occurred while getting completion: {e}")
            return None
        
    def get_completion_stream(self, messages, model, **kwargs):
        """Get completion stream from the selected AI client.

        Args:
            messages (list): List of messages.
            model (str): Model for completion.
            **kwargs: Additional keyword arguments.

        Returns:
            generator: Stream of sentences or clipboard text chunks generated by the AI client, 
                    or None if an error occurs.
        """
        try:
            completion_stream = self.client.stream_completion(messages, model, **kwargs)
            return completion_stream

        except Exception as e:
            if self.verbose:
                import traceback
                traceback.print_exc()
            else:
                print(f"An error occurred while getting completion: {e}")
            return None
        
    def process_text_stream(self, text_stream, tts_callback=None, marker_tuples=None):
        """
        This takes in a stream of text, it will search for text between the markers and pass it to the designated callback functions if provided.
        Text between markers will be removed from the stream before being passed to the tts_callback function.
        

        Args:
            text_stream: An iterable providing chunks of text.
            tts_callback: Optional callback function for sentences to be passed to.
            marker_tuples: Optional list of tuples (start_marker, end_marker, callback_function).

        Returns:
            str: The full, unmodified input text.
        """
        full_text = ""
        buffer = ""
        active_markers = []
        sentence_pattern = re.compile(r'(.*?[.!?](?:\s|$)|\n)', re.DOTALL)

        def process_active_markers():
            nonlocal buffer
            for i, (start, end, callback) in enumerate(active_markers):
                if end in buffer:
                    marked_text, _, rest = buffer.partition(end)
                    if marked_text.strip():
                        if callback:
                            callback(marked_text)
                        buffer = rest
                        return i
            return -1

        def process_new_markers_or_sentences():
            nonlocal buffer
            if marker_tuples:
                for start, end, callback in marker_tuples:
                    if start in buffer:
                        _, _, buffer = buffer.partition(start)
                        active_markers.append((start, end, callback))
                        return True
            match = sentence_pattern.match(buffer)
            if match:
                sentence = match.group(1)
                if tts_callback and sentence.strip():
                    tts_callback(sentence.strip())
                buffer = buffer[len(sentence):]
                return True
            return False

        for chunk in text_stream:
            full_text += chunk
            buffer += chunk
            
            while buffer:
                if active_markers:
                    marker_index = process_active_markers()
                    if marker_index >= 0:
                        active_markers.pop(marker_index)
                    else:
                        break
                else:
                    if not process_new_markers_or_sentences():
                        break

        # Process any remaining buffer
        while buffer:
            if active_markers:
                active_markers.pop(0)
            else:
                if tts_callback and buffer.strip():
                    tts_callback(buffer.strip())
                break

        return full_text