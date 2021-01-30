#
# EPITECH PROJECT, 2020
# Makefile
# File description:
# A Makefile turning challenge files into executables and generating frequency
# file
#

CHALLENGES_COUNT	=	14

CHALLENGES			=	$(shell seq -f "challenge%02g" 1 $(CHALLENGES_COUNT))

LONG_TEXT_FILE		=	text.txt

FREQUENCIES_FILE	=	english_chars_frequencies.txt

.SILENT:

all: $(FREQUENCIES_FILE) $(CHALLENGES)
	printf "\nGenerated $(CHALLENGES_COUNT) challenge files\n"
	printf "\nFIY, latest commits were:\n\n"
	git log | head -n 24

challenge%:
	printf "Generating $@\n"
	cat .CHALLENGE_TEMPLATE | sed s/\$$NAME/$@/g > $@
	chmod +x $@

$(FREQUENCIES_FILE):
	printf "\nGenerating $(FREQUENCIES_FILE)..."
	./compute_chars_frequencies.py $(LONG_TEXT_FILE) > $(FREQUENCIES_FILE)
	printf " Complete!\n\n"

install:
	pip install -r requirements.txt

fclean:
	printf "Removing challenge and frequency files\n"
	$(RM) $(CHALLENGES)
	$(RM) $(FREQUENCIES_FILE)

re: fclean all

.PHONY: all fclean re install
