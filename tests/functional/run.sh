#!/bin/bash

ARGC=$#
ARGV=$@
RESULT_OK="\e[0;32mOK\e[0;0m"
RESULT_KO="\e[0;31mKO\e[0;0m"
RESULT_TIMED_OUT="\e[0;35mTIMED OUT\e[0;0m"
RESULT_FAILED="\e[0;35mFAILED\e[0;0m"
RESULT_SKIPPED="\e[0;36mSKIPPED\e[0;0m"
SERVER_CONFIG="tests/functional/server/config.json"
SERVER_PATH="tests/functional/server/run.py"
TOTAL=0
PASSED=0
FAILED=0
TIMEOUT=30

function cleanup {
    rm -f .out.txt
    rm -f .result.txt
}

function test {
    CHALLENGE="$1"
    NAME="$2"
    ARGS="$3"
    EXPECTED_EXIT_CODE="$4"
    OUT_PATH="./tests/functional/outputs/$CHALLENGE/$NAME.txt"

    printf "%-42s" "    Test $NAME: "
    if [[ "$ARGC" != "0" && "$ARGV" != *"$CHALLENGE"* ]]; then
        printf "$RESULT_SKIPPED\n"
        cleanup; return
    fi
    TOTAL=$(($TOTAL + 1))
    echo "./$CHALLENGE $ARGS" | timeout --foreground $TIMEOUT bash - > .out.txt 2> /dev/null
    EXIT_CODE=$?

    if [[ $EXIT_CODE == 124 ]]; then
        printf "$RESULT_TIMED_OUT\n      $TIMEOUT-sec timeout exceeded.\n"
        cleanup; return
    fi
    if [[ $EXIT_CODE == 130 ]]; then
        printf " - $RESULT_SKIPPED\n    received SIGINT\n"
        TOTAL=$(($TOTAL - 1))
        cleanup; return
    fi
    if [[ $EXIT_CODE != $EXPECTED_EXIT_CODE ]]; then
        printf "$RESULT_KO\n    Expected return code $EXPECTED_EXIT_CODE, got $EXIT_CODE\n"
        cleanup; return
    fi
    if [[ $EXIT_CODE != 0 ]]; then
        printf "$RESULT_OK\n"
        PASSED=$(($PASSED + 1))
        cleanup; return
    fi
    if [[ ! -f $OUT_PATH ]]; then
        printf "$RESULT_FAILED\n    Output file not found\n"
        return
    fi

    diff $OUT_PATH -y .out.txt > .result.txt
    DIFF_RET=$?
    [ "$DIFF_RET" != "0" ] \
        && (printf "$RESULT_KO\n    Invalid output:\n"; \
            cat .result.txt | awk '{print "\t"$0}') \
        || printf "$RESULT_OK\n"
    [ "$DIFF_RET" == "0" ] && PASSED=$(($PASSED + 1))
    cleanup
    return $DIFF_RET
}

echo "======== Starting server ========"
    ./$SERVER_PATH &> /dev/null &
    SERVER_PID=$!
    echo "  Server started (pid $SERVER_PID)"
echo

echo "======== Executing tests ========"
echo "[Challenge 01]"
    INPUTS_PATH="./tests/functional/inputs/challenge01/"
    echo "  [Subject examples]"
        test "challenge01" "example" "$INPUTS_PATH/example.txt" 0
        test "challenge01" "invalid_example_a" "$INPUTS_PATH/invalid_example_a.txt" 84
        test "challenge01" "invalid_example_b" "$INPUTS_PATH/invalid_example_b.txt" 84
    echo "  [Basic]"
        test "challenge01" "coffee" "$INPUTS_PATH/coffee.txt" 0
    echo "  [Advanced]"
        test "challenge01" "lorem" "$INPUTS_PATH/lorem.txt" 0
    echo "  [Rigor]"
        test "challenge01" "empty" "$INPUTS_PATH/empty.txt" 84
        test "challenge01" "invalid_multiline" "$INPUTS_PATH/invalid_multiline.txt" 84
        test "challenge01" "invalid_case" "$INPUTS_PATH/invalid_case.txt" 84
        test "challenge01" "invalid_character" "$INPUTS_PATH/invalid_character.txt" 84
        test "challenge01" "invalid_size" "$INPUTS_PATH/invalid_size.txt" 84
echo

echo "[Challenge 02]"
    INPUTS_PATH="./tests/functional/inputs/challenge02/"
    echo "  [Subject example]"
        test "challenge02" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [Basic]"
        test "challenge02" "coffee" "$INPUTS_PATH/coffee.txt" 0
    echo "  [Advanced]"
        test "challenge02" "long" "$INPUTS_PATH/long.txt" 0
        test "challenge02" "longer" "$INPUTS_PATH/longer.txt" 0
        test "challenge02" "longest" "$INPUTS_PATH/longest.txt" 0
    echo "  [Rigor]"
        test "challenge02" "different_sizes" "$INPUTS_PATH/different_sizes.txt" 84
echo

echo "[Challenge 03]"
    INPUTS_PATH="./tests/functional/inputs/challenge03/"
    echo "  [Subject example]"
        test "challenge03" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [Long text]"
        test "challenge03" "long_rasputin" "$INPUTS_PATH/long_rasputin.txt" 0
        test "challenge03" "long_i_will_survive" "$INPUTS_PATH/long_i_will_survive.txt" 0
    echo "  [Medium text]"
        test "challenge03" "medium_the_calling" "$INPUTS_PATH/medium_the_calling.txt" 0
        test "challenge03" "medium_monody" "$INPUTS_PATH/medium_monody.txt" 0
        test "challenge03" "medium_the_sun" "$INPUTS_PATH/medium_the_sun.txt" 0
        test "challenge03" "medium_1273" "$INPUTS_PATH/medium_1273.txt" 0
    echo "  [Short text]"
        test "challenge03" "short_pokemon" "$INPUTS_PATH/short_pokemon.txt" 0
        test "challenge03" "short_darkness" "$INPUTS_PATH/short_darkness.txt" 0
    echo "  [Rigor]"
        test "challenge03" "invalid_random" "$INPUTS_PATH/invalid_random.txt" 84
echo

echo "[Challenge 04]"
    INPUTS_PATH="./tests/functional/inputs/challenge04/"
    echo "  [Subject example]"
        test "challenge04" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [50 lines]"
        test "challenge04" "long_rasputin" "$INPUTS_PATH/long_rasputin.txt" 0
        test "challenge04" "long_i_will_survive" "$INPUTS_PATH/long_i_will_survive.txt" 0
    echo "  [100 lines]"
        test "challenge04" "medium_the_calling" "$INPUTS_PATH/medium_the_calling.txt" 0
        test "challenge04" "medium_monody" "$INPUTS_PATH/medium_monody.txt" 0
        test "challenge04" "medium_the_sun" "$INPUTS_PATH/medium_the_sun.txt" 0
        test "challenge04" "medium_1273" "$INPUTS_PATH/medium_1273.txt" 0
    echo "  [500 lines]"
        test "challenge04" "short_pokemon" "$INPUTS_PATH/short_pokemon.txt" 0
        test "challenge04" "short_darkness" "$INPUTS_PATH/short_darkness.txt" 0
    echo "  [Rigor]"
        test "challenge04" "invalid_random" "$INPUTS_PATH/invalid_random.txt" 84
echo

echo "[Challenge 05]"
    INPUTS_PATH="./tests/functional/inputs/challenge05/"
    echo "  [Subject example]"
        test "challenge05" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [Special cases]"
        test "challenge05" "one_byte_key" "$INPUTS_PATH/one_byte_key.txt" 0
        test "challenge05" "longer_key" "$INPUTS_PATH/longer_key.txt" 0
        test "challenge05" "mixed_lengths" "$INPUTS_PATH/mixed_lengths.txt" 0
    echo "  [Advanced tests]"
        test "challenge05" "advanced_a" "$INPUTS_PATH/advanced_a.txt" 0
        test "challenge05" "advanced_b" "$INPUTS_PATH/advanced_b.txt" 0
    echo "  [Rigor]"
        test "challenge05" "invalid_single_line" "$INPUTS_PATH/invalid_single_line.txt" 84
        test "challenge05" "empty_key" "$INPUTS_PATH/empty_key.txt" 84
echo

echo "[Challenge 06]"
    INPUTS_PATH="./tests/functional/inputs/challenge06/"
    echo "  [Subject example]"
        test "challenge06" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [Long text]"
        test "challenge06" "ratio_61_rasputin" "$INPUTS_PATH/ratio_61_rasputin.txt" 0
        test "challenge06" "ratio_56_i_will_survive" "$INPUTS_PATH/ratio_56_i_will_survive.txt" 0
    echo "  [Medium text]"
        test "challenge06" "ratio_54_the_calling" "$INPUTS_PATH/ratio_54_the_calling.txt" 0
        test "challenge06" "ratio_43_monody" "$INPUTS_PATH/ratio_43_monody.txt" 0
        test "challenge06" "ratio_36_the_sun" "$INPUTS_PATH/ratio_36_the_sun.txt" 0
        test "challenge06" "ratio_34_1273" "$INPUTS_PATH/ratio_34_1273.txt" 0
    echo "  [Short text]"
        test "challenge06" "ratio_23_pokemon" "$INPUTS_PATH/ratio_23_pokemon.txt" 0
        test "challenge06" "ratio_14_darkness" "$INPUTS_PATH/ratio_14_darkness.txt" 0
    echo "  [Low ratio, long key]"
        test "challenge06" "ratio_12_under_the_sea" "$INPUTS_PATH/ratio_12_under_the_sea.txt" 0
        test "challenge06" "ratio_11_prince_ali" "$INPUTS_PATH/ratio_11_prince_ali.txt" 0
    echo "  [Rigor]"
        test "challenge06" "invalid_random" "$INPUTS_PATH/invalid_random.txt" 84
echo

echo "[Challenge 07]"
    INPUTS_PATH="./tests/functional/inputs/challenge07/"
    echo "  [Subject example]"
        test "challenge07" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [AES-128]"
        test "challenge07" "8_bytes_key" "$INPUTS_PATH/8_bytes_key.txt" 0
        test "challenge07" "11_bytes_key" "$INPUTS_PATH/11_bytes_key.txt" 0
        test "challenge07" "13_bytes_key" "$INPUTS_PATH/13_bytes_key.txt" 0
    echo "  [AES-192]"
        test "challenge07" "18_bytes_key" "$INPUTS_PATH/18_bytes_key.txt" 0
        test "challenge07" "24_bytes_key" "$INPUTS_PATH/24_bytes_key.txt" 0
    echo "  [AES-256]"
        test "challenge07" "25_bytes_key" "$INPUTS_PATH/25_bytes_key.txt" 0
        test "challenge07" "32_bytes_key" "$INPUTS_PATH/32_bytes_key.txt" 0
    echo "  [Rigor]"
        test "challenge07" "empty_file" "$INPUTS_PATH/empty_file.txt" 84
        test "challenge07" "too_long_key" "$INPUTS_PATH/too_long_key.txt" 84
echo

echo "[Challenge 08]"
    INPUTS_PATH="./tests/functional/inputs/challenge08/"
    echo "  [Subject example]"
        test "challenge08" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [AES-128]"
        test "challenge08" "aes_128_a" "$INPUTS_PATH/aes_128_a.txt" 0
        test "challenge08" "aes_128_b" "$INPUTS_PATH/aes_128_b.txt" 0
        test "challenge08" "aes_128_c" "$INPUTS_PATH/aes_128_c.txt" 0
    echo "  [AES-192]"
        test "challenge08" "aes_192_a" "$INPUTS_PATH/aes_192_a.txt" 0
        test "challenge08" "aes_192_b" "$INPUTS_PATH/aes_192_b.txt" 0
        test "challenge08" "aes_192_c" "$INPUTS_PATH/aes_192_c.txt" 0
    echo "  [AES-256]"
        test "challenge08" "aes_256_a" "$INPUTS_PATH/aes_256_a.txt" 0
        test "challenge08" "aes_256_b" "$INPUTS_PATH/aes_256_b.txt" 0
        test "challenge08" "aes_256_c" "$INPUTS_PATH/aes_256_c.txt" 0
    echo "  [Big cases]"
        test "challenge08" "aes_128_big" "$INPUTS_PATH/aes_128_big.txt" 0
        test "challenge08" "aes_192_big" "$INPUTS_PATH/aes_192_big.txt" 0
        test "challenge08" "aes_256_big" "$INPUTS_PATH/aes_256_big.txt" 0
    echo "  [Rigor]"
        test "challenge08" "empty_file" "$INPUTS_PATH/empty_file.txt" 84
        test "challenge08" "invalid_block_size" "$INPUTS_PATH/invalid_block_size.txt" 84
        test "challenge08" "invalid_random" "$INPUTS_PATH/invalid_random.txt" 84
echo

echo "[Challenge 09]"
    INPUTS_PATH="./tests/functional/inputs/challenge09/"
    echo "  [Subject example]"
        test "challenge09" "example" "$INPUTS_PATH/example.txt" 0
    echo "  [Basic]"
        test "challenge09" "basic" "$INPUTS_PATH/basic.txt" 0
    echo "  [Different key sizes]"
        test "challenge09" "cbc_128" "$INPUTS_PATH/cbc_128.txt" 0
        test "challenge09" "cbc_192" "$INPUTS_PATH/cbc_192.txt" 0
        test "challenge09" "cbc_256" "$INPUTS_PATH/cbc_256.txt" 0
    echo "  [Rigor]"
        test "challenge09" "empty_file" "$INPUTS_PATH/empty_file.txt" 84
        test "challenge09" "invalid_key_size" "$INPUTS_PATH/invalid_key_size.txt" 84
        test "challenge09" "invalid_vector_size" "$INPUTS_PATH/invalid_vector_size.txt" 84
echo

echo "[Challenge 10]"
    INPUTS_PATH="./tests/functional/inputs/challenge10/"
    echo "  [Subject example]"
        cp "$INPUTS_PATH/example.txt" $SERVER_CONFIG
        test "challenge10" "example" "" 0
    echo "  [Single block text]"
        cp "$INPUTS_PATH/8_chars.txt" $SERVER_CONFIG
        test "challenge10" "8_chars" "" 0
        cp "$INPUTS_PATH/12_chars.txt" $SERVER_CONFIG
        test "challenge10" "12_chars" "" 0
    echo "  [Multiblock text]"
        cp "$INPUTS_PATH/21_chars.txt" $SERVER_CONFIG
        test "challenge10" "21_chars" "" 0
        cp "$INPUTS_PATH/32_chars.txt" $SERVER_CONFIG
        test "challenge10" "32_chars" "" 0
    echo "  [Rigor]"
        cp "$INPUTS_PATH/empty.txt" $SERVER_CONFIG
        test "challenge10" "empty" "" 84
echo

echo "[Challenge 11]"
    INPUTS_PATH="./tests/functional/inputs/challenge11/"
    echo "  [Random keys]"
        cp "$INPUTS_PATH/test_a.txt" $SERVER_CONFIG
        test "challenge11" "test_a" "" 0
        cp "$INPUTS_PATH/test_b.txt" $SERVER_CONFIG
        test "challenge11" "test_b" "" 0
        cp "$INPUTS_PATH/test_c.txt" $SERVER_CONFIG
        test "challenge11" "test_c" "" 0
        cp "$INPUTS_PATH/test_d.txt" $SERVER_CONFIG
        test "challenge11" "test_d" "" 0
        cp "$INPUTS_PATH/test_e.txt" $SERVER_CONFIG
        test "challenge11" "test_e" "" 0
    echo "  [Rigor]"
        cp "$INPUTS_PATH/empty.txt" $SERVER_CONFIG
        test "challenge11" "empty" "" 84
echo

echo "[Challenge 12]"
    INPUTS_PATH="./tests/functional/inputs/challenge12/"
    echo "  [Subject example]"
        cp "$INPUTS_PATH/example.txt" $SERVER_CONFIG
        test "challenge12" "example" "" 0
    echo "  [Single block prefix and suffix]"
        cp "$INPUTS_PATH/prefix_4_suffix_8.txt" $SERVER_CONFIG
        test "challenge12" "prefix_4_suffix_8" "" 0
        cp "$INPUTS_PATH/prefix_8_suffix_8.txt" $SERVER_CONFIG
        test "challenge12" "prefix_8_suffix_8" "" 0
        cp "$INPUTS_PATH/prefix_11_suffix_12.txt" $SERVER_CONFIG
        test "challenge12" "prefix_11_suffix_12" "" 0
        cp "$INPUTS_PATH/prefix_15_suffix_12.txt" $SERVER_CONFIG
        test "challenge12" "prefix_15_suffix_12" "" 0
    echo "  [Multiblock prefix and suffix]"
        cp "$INPUTS_PATH/prefix_17_suffix_21.txt" $SERVER_CONFIG
        test "challenge12" "prefix_17_suffix_21" "" 0
        cp "$INPUTS_PATH/prefix_28_suffix_21.txt" $SERVER_CONFIG
        test "challenge12" "prefix_28_suffix_21" "" 0
        cp "$INPUTS_PATH/prefix_32_suffix_32.txt" $SERVER_CONFIG
        test "challenge12" "prefix_32_suffix_32" "" 0
        cp "$INPUTS_PATH/prefix_50_suffix_32.txt" $SERVER_CONFIG
        test "challenge12" "prefix_50_suffix_32" "" 0
    echo "  [Rigor]"
        cp "$INPUTS_PATH/empty_suffix.txt" $SERVER_CONFIG
        test "challenge12" "empty_suffix" "" 0
        cp "$INPUTS_PATH/empty_suffix_and_prefix.txt" $SERVER_CONFIG
        test "challenge12" "empty_suffix_and_prefix" "" 0
echo

echo "[Challenge 13]"
    INPUTS_PATH="./tests/functional/inputs/challenge13/"
    echo "  [Subject example]"
        cp "$INPUTS_PATH/example.txt" $SERVER_CONFIG
        test "challenge13" "example" "" 0
    echo "  [Random keys]"
        cp "$INPUTS_PATH/test_a.txt" $SERVER_CONFIG
        test "challenge13" "test_a" "" 0
        cp "$INPUTS_PATH/test_b.txt" $SERVER_CONFIG
        test "challenge13" "test_b" "" 0
        cp "$INPUTS_PATH/test_c.txt" $SERVER_CONFIG
        test "challenge13" "test_c" "" 0
        cp "$INPUTS_PATH/test_d.txt" $SERVER_CONFIG
        test "challenge13" "test_d" "" 0
        cp "$INPUTS_PATH/test_e.txt" $SERVER_CONFIG
        test "challenge13" "test_e" "" 0
        cp "$INPUTS_PATH/test_f.txt" $SERVER_CONFIG
        test "challenge13" "test_f" "" 0
    echo "  [Rigor]"
        cp "$INPUTS_PATH/empty.txt" $SERVER_CONFIG
        test "challenge13" "empty" "" 84
echo

echo "[Challenge 14]"
    INPUTS_PATH="./tests/functional/inputs/challenge14/"
    echo "  [Single block]"
        cp "$INPUTS_PATH/single_block_a.txt" $SERVER_CONFIG
        test "challenge14" "single_block_a" "" 0
        cp "$INPUTS_PATH/single_block_b.txt" $SERVER_CONFIG
        test "challenge14" "single_block_b" "" 0
        cp "$INPUTS_PATH/single_block_full.txt" $SERVER_CONFIG
        test "challenge14" "single_block_full" "" 0
    echo "  [Double block]"
        cp "$INPUTS_PATH/double_block_a.txt" $SERVER_CONFIG
        test "challenge14" "double_block_a" "" 0
        cp "$INPUTS_PATH/double_block_b.txt" $SERVER_CONFIG
        test "challenge14" "double_block_b" "" 0
        cp "$INPUTS_PATH/double_block_full.txt" $SERVER_CONFIG
        test "challenge14" "double_block_full" "" 0
    echo "  [Rigor]"
        cp "$INPUTS_PATH/empty.txt" $SERVER_CONFIG
        test "challenge14" "empty" "" 84
    echo "  [FATALITY]"
        cp "$INPUTS_PATH/fatality.txt" $SERVER_CONFIG
        test "challenge14" "fatality" "" 0
echo

echo "======== Stopping server ========"
    kill $SERVER_PID
    wait $SERVER_PID 2> /dev/null
    echo "  Server stopped (pid $SERVER_PID)"
echo

printf "\nRESULT:\n"
printf "  $PASSED / $TOTAL\n"
printf "  $(printf $(($PASSED * 10000 / $TOTAL)) | sed 's/..$/.&/') %%\n"
if [[ $FAILED != "0" ]]; then
    printf "\nWARNING!!! $FAILED test(s) failed\n"
    exit 1
fi
[ $PASSED != $TOTAL ] && exit 1 || exit 0
