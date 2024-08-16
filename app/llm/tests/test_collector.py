from django.test import TestCase
from django.core.management import call_command
from cvitae.settings import INSTALLED_APPS, BASE_DIR
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
import requests
import os
import logging
from urllib import parse
import json

logger = logging.getLogger(__name__)

# Create your tests here.


class PrimaryTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        # client
        self.LLM_IP = "192.168.179.4"
        self.LLM_URL = f"http://{self.LLM_IP}/api/generate"
        self.HOST_URL = "http://localhost:8000"

    def post_prompt(self, prompt):
        """tested with ollama api"""
        return requests.post(
            self.LLM_URL,
            json={
                "stream": False,
                "model": "llama3",
                "prompt": prompt,
                "format": "json",
                "options": {
                    "num_keep": 2,
                    "seed": 2,
                    "num_predict": 90,
                    "temperature": 0.2,
                    "top_k": 20,
                    # "top_p": 0.9,
                    # "min_p": 0.0,
                    # "tfs_z": 0.5,
                    # "typical_p": 0.7,
                    # "repeat_last_n": 33,
                    # "repeat_penalty": 1.2,
                    # "presence_penalty": 1.5,
                    # "frequency_penalty": 1.0,
                    # "mirostat": 1,
                    # "mirostat_tau": 0.8,
                    # "mirostat_eta": 0.6,
                    # "penalize_newline": True,
                    # "stop": ["\n", "user:"],
                    # "numa": False,
                    # "num_ctx": 1024,
                    # "num_batch": 2,
                    # "num_gpu": 1,
                    # "main_gpu": 0,
                    # "low_vram": False,
                    # "f16_kv": True,
                    # "vocab_only": False,
                    # "use_mmap": True,
                    # "use_mlock": False,
                    # "num_thread": 8,
                },
            },
        )

    def disable_test_llm_connection(self):

        response = self.post_prompt("Count from 1 to 5 and return json array")
        logger.warn([response, response.json()["response"]])

    def test_production_api(self):
        # this test call the production api and databse outside the test environment
        # prompt_id points to an instance in collector promtclient table
        prompt_id = "1"
        collector_url = parse.urljoin(self.HOST_URL, reverse("llm_collector-list"))
        logger.warn(collector_url)
        collector_list = requests.get(collector_url)
        llm_urls = collector_list.json()
        prompt_url = parse.urljoin(llm_urls["prompt"], f"{prompt_id}/")
        prompt_client = requests.get(prompt_url).json()
        result = self.post_prompt(prompt_client["template"])
        try:
            data = json.loads(result.json()["response"])
            # data = json.dumps(data, indent=2)
            logger.warn("data")
            logger.warn(data)
            logger.warn(prompt_url)
            res = requests.put(
                prompt_url,
                headers={"content-type": "application/json"},
                json={"response_json": data},
            )
            logger.warn(res.status_code)
            logger.warn("res.json ##############")
            logger.warn(res.json())
        except Exception as e:
            logger.warn("FAIL #########")
            logger.warn(e)
            logger.warn(result)
