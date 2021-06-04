from dataclasses import dataclass
from datetime import date
import mock
from pdfminer.layout import LTChar, LTFigure, LTImage, LTTextBoxHorizontal, LTTextLineHorizontal
from typing import List

from rdr_service.services import consent_files
from tests.helpers.unittest_base import BaseTestCase


class ConsentFileParsingTest(BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(ConsentFileParsingTest, self).__init__(*args, **kwargs)
        self.uses_database = False

    def test_vibrent_primary_consent(self):
        for consent_example in self._get_vibrent_primary_test_data():
            consent_file = consent_example.file
            self.assertEqual(consent_example.expected_signature, consent_file.get_signature_on_file())
            self.assertEqual(consent_example.expected_sign_date, consent_file.get_date_signed())
            self.assertEqual(consent_example.expected_to_be_va_file, consent_file.get_is_va_consent())

    def _get_vibrent_primary_test_data(self) -> List['PrimaryConsentTestData']:
        """
        Builds a list of PDFs that represent the different layouts of Vibrent's primary consent
        that have been encountered. Add to this if the code incorrectly parses any Vibrent primary pdf
        """
        test_data = []

        # reusable elements usually expected on the signature page
        description_elements = [
            self._build_pdf_element(
                cls=LTTextBoxHorizontal,
                children=[
                    self._build_pdf_element(
                        cls=LTTextLineHorizontal,
                        text='understand the information in this form. All of my questions\n'
                    ),
                    self._build_pdf_element(
                        cls=LTTextLineHorizontal,
                        text='have been answered. I freely and willingly choose to take part in\n'
                    ),
                    self._build_pdf_element(
                        cls=LTTextLineHorizontal,
                        text='the All of Us Research Program.\n'
                    )
                ]
            ),
            self._build_pdf_element(
                cls=LTTextBoxHorizontal,
                children=[
                    self._build_pdf_element(cls=LTTextLineHorizontal, text='Sign Your Full Name: \n')
                ]
            )
        ]

        # Build basic file with signature of Test Name and signing date of August 17, 2019
        pdf = self._build_pdf(pages=[
            [
                *description_elements,
                self._build_form_element(text='Test Name', bbox=(116.734, 147.229, 517.202, 169.229)),
                self._build_form_element(text='Aug 17, 2019', bbox=(116.167, 97.3622, 266.167, 119.362))
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature='Test Name',
                expected_sign_date=date(2019, 8, 17)
            )
        )

        # Build an older style of primary layout, with signature box higher up on the page
        pdf = self._build_pdf(pages=[
            [
                *description_elements,
                self._build_form_element(text='Nick', bbox=(116, 585, 517, 605)),
                self._build_form_element(text='Dec 25, 2017', bbox=(116, 565, 266, 585))
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature='Nick',
                expected_sign_date=date(2017, 12, 25)
            )
        )

        # Build basic VA primary file
        pdf = self._build_pdf(pages=[
            [
                self._build_pdf_element(
                    cls=LTTextBoxHorizontal,
                    children=[
                        self._build_pdf_element(cls=LTTextLineHorizontal, text='you will get care at a VA facility')
                    ]
                )
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature=None,
                expected_sign_date=None,
                expected_to_be_va_file=True
            )
        )

        # Build file with an empty text element instead of a signature and date
        pdf = self._build_pdf(pages=[
            [
                *description_elements,
                self._build_form_element(text='', bbox=(116.16, 147.48, 521.16, 171.240)),
                self._build_form_element(text='', bbox=(116.167, 97.3622, 266.167, 119.362))
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature=None,
                expected_sign_date=None
            )
        )

        # Build consent with an image instead of a typed signature
        pdf = self._build_pdf(pages=[
            [
                *description_elements,
                self._build_form_element(
                    bbox=(200.0, 125.0, 400.0, 191.595),
                    children=[
                        self._build_pdf_element(cls=LTImage, bbox=(200.0, 125.0, 400.0, 191.595))
                    ]
                ),
                self._build_form_element(text='December 7, 2018', bbox=(116.167, 97.3622, 266.167, 119.362))
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature=True,
                expected_sign_date=date(2018, 12, 7)
            )
        )

        # Build older style consent with different signature description formatting
        pdf = self._build_pdf(pages=[
            [
                self._build_pdf_element(
                    cls=LTTextBoxHorizontal,
                    children=[
                        self._build_pdf_element(
                            cls=LTTextLineHorizontal,
                            text='this form. All of my questions have been answered. I freely and\n'
                        ),
                        self._build_pdf_element(
                            cls=LTTextLineHorizontal,
                            text='willingly choose to take part in the All of Us Research Program.\n'
                        ),
                    ]
                ),
                self._build_pdf_element(
                    cls=LTTextBoxHorizontal,
                    children=[
                        self._build_pdf_element(
                            cls=LTTextLineHorizontal,
                            children=[
                                self._build_pdf_element(LTTextLineHorizontal, text='Sign Your \n'),
                                self._build_pdf_element(LTTextLineHorizontal, text='Full Name: \n')
                            ]
                        )
                    ]
                ),
                self._build_form_element(text='2018 Participant', bbox=(116.16, 147.48, 521.16, 171.24)),
                self._build_form_element(text='Feb 19, 2018', bbox=(116.16, 96.84, 521.16, 120.6))
            ]
        ])
        test_data.append(
            PrimaryConsentTestData(
                file=consent_files.VibrentPrimaryConsentFile(pdf),
                expected_signature='2018 Participant',
                expected_sign_date=date(2018, 2, 19)
            )
        )

        return test_data

    @classmethod
    def _build_pdf(cls, pages) -> consent_files.Pdf:
        """
        Builds a consent_files.Pdf object
        :param pages A list where each item represents a page,
            and each item is a list of pdf elements for what should be on that page
        """
        page_mocks = []
        for page_elements in pages:
            page_mock = mock.MagicMock()
            page_mock.__iter__.return_value = page_elements
            page_mocks.append(page_mock)

        return consent_files.Pdf(pages=page_mocks)

    def _build_pdf_element(self, cls, text: str = None, children: list = None, bbox=None):
        """Create a generic pdf element to add to the page"""
        element = mock.MagicMock(spec=cls)
        self._set_bbox(bbox, element)

        if children:
            element.__iter__.return_value = children

        if hasattr(element, 'get_text'):
            if text is None:
                get_text_result = ''.join([child.get_text() for child in children])
            else:
                get_text_result = text
            element.get_text.return_value = get_text_result

        return element

    def _build_form_element(self, bbox, text: str = None, children: list = None):
        """
        Form elements don't have a get_text method, and (at least with the Vibrent PDFs) any text within them is
        laid out character by character
        """
        element = mock.MagicMock(spec=LTFigure)
        self._set_bbox(bbox, element)

        if children:
            element.__iter__.return_value = children
        else:
            char_list = []
            for char_str in text:
                char_element = mock.MagicMock(spec=LTChar)
                char_element.get_text.return_value = char_str
                char_list.append(char_element)
            if text == '':
                char_element = mock.MagicMock(spec=LTChar)
                char_element.get_text.return_value = ''
                char_list.append(char_element)
            element.__iter__.return_value = char_list

        return element

    def _set_bbox(self, bbox, element_mock):
        """Set the data for a PDF element's bounding box on the Mock object"""
        if not bbox:
            left, bottom = self.fake.random_int(), self.fake.random_int()
            right, top = self.fake.random_int() + left, self.fake.random_int() + bottom
            bbox = (left, bottom, right, top)

        (x0, y0, x1, y1) = bbox
        element_mock.x0 = x0
        element_mock.y0 = y0
        element_mock.x1 = x1
        element_mock.y1 = y1
        element_mock.width = x1-x0
        element_mock.height = y1-y0
        element_mock.bbox = bbox


@dataclass
class ConsentTestData:
    file: consent_files.ConsentFile
    expected_signature: str or bool  # Text of the signature, or True if it's an image
    expected_sign_date: date or None


@dataclass
class PrimaryConsentTestData(ConsentTestData):
    file: consent_files.PrimaryConsentFile
    expected_to_be_va_file: bool = False
