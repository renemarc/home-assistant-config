#
# Markdownlint style guide
#
# Link: https://github.com/markdownlint/markdownlint/blob/master/docs/RULES.md
#

# Enforce all rules
all

# Configure rules
rule 'MD007', :indent => 4          # Unordered list indentation
rule 'MD029', :style => :Ordered    # Ordered list item prefix

# Exclude rules
exclude_rule 'MD002' # First header should be a top level header
exclude_rule 'MD013' # Line length
exclude_rule 'MD033' # Inline HTML
exclude_rule 'MD039' # Spaces inside link text
exclude_rule 'MD041' # First line in file should be a top level header
