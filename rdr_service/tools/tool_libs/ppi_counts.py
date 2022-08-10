import json

from sqlalchemy import and_

from rdr_service.tools.tool_libs.tool_base import cli_run, ToolBase

from rdr_service.model.participant import Participant
from rdr_service.services.system_utils import list_chunks


tool_cmd = 'ppi_script'
tool_desc = 'counting ppi modules'


class Script(ToolBase):
    logger_name = None

    def _get_or_init(self, map_store, key, constructor):
        if key not in map_store:
            map_store[key] = constructor()

        return map_store[key]

    def run(self):
        super(Script, self).run()

        #####################
        # UNCOMMENT THIS TO PROCESS THE FILE (and be sure to comment out the rest)
        #####################
        # with open('pii_summary_output.json') as file:
        #     file_str = file.read()
        #     json_data = json.loads(file_str)
        #
        #     for module_name, participant_response_map in json_data.items():
        #         count = 0
        #         for response_list in participant_response_map.values():
        #             count += len(response_list)
        #         print(f'{module_name}: {count}')
        # return



        from rdr_service.model.code import Code
        from rdr_service.model.participant_summary import ParticipantSummary
        from rdr_service.model.questionnaire import QuestionnaireConcept
        from rdr_service.model.questionnaire_response import QuestionnaireResponse

        module_pid_hash_map = {}

        with self.get_session() as session:

            # get the participants
            participant_id_list = session.query(
                ParticipantSummary.participantId
            ).join(
                Participant
            ).filter(
                Participant.isTestParticipant != 1,
                Participant.hpoId != 21
            ).all()
            participant_id_list = [participant.participantId for participant in participant_id_list]

            # for each participant, get their responses (with answer hash, and what the module was)
            count = 0
            for id_chunk in list_chunks(participant_id_list, 1000):
                print(f'{count} of {len(participant_id_list)}')
                count += 1000

                response_query = session.query(
                    QuestionnaireResponse.participantId,
                    QuestionnaireResponse.answerHash,
                    QuestionnaireResponse.authored,
                    Code.value
                ).join(
                    QuestionnaireConcept,
                    and_(
                        QuestionnaireConcept.questionnaireId == QuestionnaireResponse.questionnaireId,
                        QuestionnaireConcept.questionnaireVersion == QuestionnaireResponse.questionnaireVersion
                    )
                ).join(
                    Code,
                    Code.codeId == QuestionnaireConcept.codeId
                ).filter(
                    QuestionnaireResponse.status == 1,
                    QuestionnaireResponse.classificationType == 0,
                    QuestionnaireResponse.participantId.in_(id_chunk),
                    Code.value.in_([
                        'TheBasics',
                        'OverallHealth',
                        'Lifestyle',
                        'FamilyHistory',
                        'HealthcareAccess',
                        'PersonalMedicalHistory',
                        'MedicationsPPI',
                        'cope',
                        'cope_nov',
                        'cope_dec',
                        'cope_jan',
                        'cope_feb',
                        'cope_vaccine1',
                        'cope_vaccine2',
                        'cope_vaccine3',
                        'cope_vaccine4',
                        'sdoh',
                        'personalfamilyhistory'
                    ])
                )

                # for each response, store the answer hash in a set by module type
                for participant_id, answer_hash, authored, module_code in response_query.all():
                    pid_hash_map = self._get_or_init(
                        map_store=module_pid_hash_map,
                        key=module_code,
                        constructor=dict
                    )
                    hash_authored_map = self._get_or_init(
                        map_store=pid_hash_map,
                        key=participant_id,
                        constructor=dict
                    )
                    if answer_hash not in hash_authored_map:
                        hash_authored_map[answer_hash] = str(authored)

            # store the results
            with open('pii_summary_output.json', 'w') as output:
                output.write(json.dumps(module_pid_hash_map))


def run():
    return cli_run(tool_cmd, tool_desc, Script)
