AFA 2027 AI Workflow Submission Template — LaTeX Template

A clean article template for an AFA 2027 AI Workflow submission. Uses natbib
for citations (\citet{} and \citep{}) and includes AFA-specific appendices for
workflow documentation.

Files:
  academic_paper_template.tex  — Main document
  template_references.bib      — Sample bibliography (replace with yours)

How to use:
  1. Copy this folder: cp -r latex_template/ paper/
  2. Edit academic_paper_template.tex (title, author, sections)
  3. Replace template_references.bib with your own .bib file
     (use Corbis export_citations to generate BibTeX entries)
  4. Fill Appendix A-D from submission/workflow.md,
     submission/initial_prompt.md, submission/model_config.md,
     submission/human_time_log.md, submission/contribution_report.md, and
     submission/conversations/README.md.
  5. Compile: pdflatex -> bibtex -> pdflatex -> pdflatex

Requires a LaTeX distribution (MacTeX, TeX Live, or MikTeX).
