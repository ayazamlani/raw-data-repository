from abc import ABC, abstractmethod
import logging
from typing import List

from rdr_service.domain_model.response import Response
from rdr_service.model.participant_summary import ParticipantSummary


class ResponseProcessor(ABC):
    @abstractmethod
    def process_response(self, response: Response, summary: ParticipantSummary):
        ...

    @classmethod
    def is_response_to_relevant_survey(cls, response: Response, survey_codes: List[str]):
        return response.survey_code.lower() in [code_str.lower() for code_str in survey_codes]

    def get_answer(self, response: Response, question_code: str):
        """
        Provide a safe way to retrieve a single answer, if multiple answers are found then the duplication is
        logged and the first answer is returned.
        """
        answer_list = response.get_answers_for(question_code_str=question_code)
        if not answer_list:
            return None

        if len(answer_list) > 1:
            logging.warning(f'Multiple answers found for {question_code}')

        return answer_list[0]

