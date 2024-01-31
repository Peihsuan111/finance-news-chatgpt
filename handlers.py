# save the below code in a file by name handler.py
# Importing the necessary packages
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import BaseMessage
from langchain.schema import LLMResult
from typing import Dict, List, Any

# import sys


# Creating the custom callback handler class
class MyCustomHandler(StreamingStdOutCallbackHandler):
    def __init__(self, queue) -> None:
        super().__init__()
        # we will be providing the streamer queue as an input
        self._queue = queue
        # defining the stop signal that needs to be added to the queue in
        # case of the last token
        self._stop_signal = None
        print("Custom handler Initialized")

    # On the arrival of the new token, we are adding the new token in the
    # queue
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self._queue.put(token)
        # sys.stdout.write(token)
        # sys.stdout.flush()

    # on the start or initialization, we just print or log a starting message
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        print("generation started")

    # On receiving the last token, we add the stop signal, which determines
    # the end of the generation
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        print("\n\ngeneration concluded")
        self._queue.put(self._stop_signal)
