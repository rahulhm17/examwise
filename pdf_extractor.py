# ============================================================
# ExamWise - PDF Text + OCR Extractor
# File: utils/pdf_extractor.py
# ============================================================

import fitz
from PIL import Image

from utils.image_extractor import extract_text_from_image


# ============================================================
# SETTINGS
# ============================================================

# If a PDF page contains less text than this, ExamWise will
# treat it as a possible scanned/image page and use OCR.
MIN_TEXT_LENGTH = 40

# Higher value = clearer page image for OCR.
OCR_ZOOM = 2.0


# ============================================================
# PDF PAGE → IMAGE
# ============================================================

def pdf_page_to_image(page):
    """
    Convert a PyMuPDF PDF page into a PIL image.

    This is used when a PDF page is scanned and does not
    contain useful selectable text.
    """

    matrix = fitz.Matrix(
        OCR_ZOOM,
        OCR_ZOOM
    )

    pixmap = page.get_pixmap(
        matrix=matrix,
        alpha=False
    )

    image = Image.frombytes(
        "RGB",
        [pixmap.width, pixmap.height],
        pixmap.samples
    )

    return image


# ============================================================
# NORMALIZE PAGE TEXT
# ============================================================

def clean_pdf_text(text):
    """
    Perform basic cleaning while preserving line structure.
    """

    if not text:
        return ""

    cleaned_lines = []

    for line in text.splitlines():

        line = " ".join(
            line.strip().split()
        )

        if line:
            cleaned_lines.append(
                line
            )

    return "\n".join(
        cleaned_lines
    )


# ============================================================
# MAIN PDF EXTRACTION FUNCTION
# ============================================================

def extract_text_from_pdf(uploaded_file):
    """
    Extract text from normal, scanned and mixed PDFs.

    Normal PDF:
        PyMuPDF text extraction

    Scanned PDF:
        PDF page → image → EasyOCR

    Mixed PDF:
        Text extraction for digital pages
        OCR for scanned pages
    """

    document = None

    try:

        # ----------------------------------------------------
        # READ PDF
        # ----------------------------------------------------

        uploaded_file.seek(0)

        pdf_bytes = uploaded_file.read()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        page_count = len(document)

        if page_count == 0:

            return {
                "success": False,
                "text": "",
                "type": "Unknown PDF",
                "page_count": 0,
                "text_pages": 0,
                "ocr_pages": 0,
                "ocr_confidence": 0.0,
                "page_details": [],
                "error": "The PDF contains no pages."
            }


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        all_page_text = []

        page_details = []

        text_pages = 0

        ocr_pages = 0

        ocr_confidences = []


        # ----------------------------------------------------
        # PROCESS EVERY PAGE
        # ----------------------------------------------------

        for page_number in range(
            page_count
        ):

            page = document[
                page_number
            ]

            # -----------------------------------------------
            # TRY NORMAL PDF TEXT EXTRACTION
            # -----------------------------------------------

            normal_text = page.get_text(
                "text"
            )

            normal_text = clean_pdf_text(
                normal_text
            )


            # ===============================================
            # TEXT PAGE
            # ===============================================

            if len(normal_text.strip()) >= MIN_TEXT_LENGTH:

                text_pages += 1

                all_page_text.append(
                    normal_text
                )

                page_details.append(
                    {
                        "page": page_number + 1,
                        "method": "Text",
                        "success": True,
                        "confidence": None,
                        "characters": len(
                            normal_text
                        )
                    }
                )

                continue


            # ===============================================
            # SCANNED PAGE → OCR
            # ===============================================

            try:

                page_image = pdf_page_to_image(
                    page
                )

                ocr_result = extract_text_from_image(
                    page_image
                )


                # -------------------------------------------
                # OCR SUCCESS
                # -------------------------------------------

                if ocr_result["success"]:

                    ocr_text = ocr_result[
                        "text"
                    ]

                    all_page_text.append(
                        ocr_text
                    )

                    ocr_pages += 1

                    confidence = ocr_result.get(
                        "confidence",
                        0.0
                    )

                    ocr_confidences.append(
                        confidence
                    )

                    page_details.append(
                        {
                            "page": page_number + 1,
                            "method": "OCR",
                            "success": True,
                            "confidence": confidence,
                            "characters": len(
                                ocr_text
                            )
                        }
                    )


                # -------------------------------------------
                # OCR FOUND NOTHING
                # -------------------------------------------

                else:

                    page_details.append(
                        {
                            "page": page_number + 1,
                            "method": "OCR",
                            "success": False,
                            "confidence": 0.0,
                            "characters": 0,
                            "error": ocr_result.get(
                                "error"
                            )
                        }
                    )


            except Exception as page_error:

                page_details.append(
                    {
                        "page": page_number + 1,
                        "method": "OCR",
                        "success": False,
                        "confidence": 0.0,
                        "characters": 0,
                        "error": str(
                            page_error
                        )
                    }
                )


        # ----------------------------------------------------
        # COMBINE TEXT
        # ----------------------------------------------------

        final_text = "\n\n".join(
            text
            for text in all_page_text
            if text.strip()
        )


        # ----------------------------------------------------
        # DETERMINE DOCUMENT TYPE
        # ----------------------------------------------------

        if text_pages == page_count:

            document_type = "Text PDF"

        elif ocr_pages == page_count:

            document_type = "Scanned PDF"

        elif (
            text_pages > 0
            and ocr_pages > 0
        ):

            document_type = "Mixed PDF"

        elif ocr_pages > 0:

            document_type = "Scanned PDF"

        elif text_pages > 0:

            document_type = "Text PDF"

        else:

            document_type = "Unreadable PDF"


        # ----------------------------------------------------
        # AVERAGE OCR CONFIDENCE
        # ----------------------------------------------------

        if ocr_confidences:

            average_ocr_confidence = (
                sum(ocr_confidences)
                /
                len(ocr_confidences)
            )

        else:

            average_ocr_confidence = 0.0


        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if final_text.strip():

            return {
                "success": True,

                "text": final_text,

                "type": document_type,

                "page_count": page_count,

                "text_pages": text_pages,

                "ocr_pages": ocr_pages,

                "ocr_confidence": round(
                    average_ocr_confidence,
                    2
                ),

                "page_details": page_details,

                "error": None
            }


        # ----------------------------------------------------
        # NO TEXT FOUND
        # ----------------------------------------------------

        return {
            "success": False,

            "text": "",

            "type": "Unreadable PDF",

            "page_count": page_count,

            "text_pages": text_pages,

            "ocr_pages": ocr_pages,

            "ocr_confidence": 0.0,

            "page_details": page_details,

            "error": (
                "ExamWise could not detect readable text "
                "in this PDF."
            )
        }


    except Exception as error:

        return {
            "success": False,

            "text": "",

            "type": "PDF Error",

            "page_count": 0,

            "text_pages": 0,

            "ocr_pages": 0,

            "ocr_confidence": 0.0,

            "page_details": [],

            "error": str(error)
        }


    finally:

        if document is not None:

            document.close()