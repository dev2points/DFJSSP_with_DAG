#!/bin/bash

# Thư mục gốc chứa các kết quả
RESULTS_DIR="results"
PYTHON_SCRIPT="verify_and_visualize.py" # Thay tên file python của bạn nếu khác

# Kiểm tra xem file script Python có tồn tại không
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "[X] Error: Cannot find Python script '$PYTHON_SCRIPT'"
    exit 1
fi


total_files=0
success_count=0
failed_count=0

for num_factories in {2..4}; do
    factory_dir="${RESULTS_DIR}/${num_factories}factories"

    if [ ! -d "$factory_dir" ]; then
        continue
    fi

    echo ""
    echo "=========================================================="
    echo "  Processing: ${num_factories} FACTORIES ($factory_dir)"
    echo "=========================================================="

    for dataset_type in "fmj" "brandimarte" "rdata"; do
        dataset_dir="${factory_dir}/${dataset_type}"

        if [ ! -d "$dataset_dir" ]; then
            continue
        fi


        shopt -s nullglob
        log_files=("${dataset_dir}"/*.log "${dataset_dir}"/*.txt)
        shopt -u nullglob

        if [ ${#log_files[@]} -eq 0 ]; then
            echo "      (Cannot find any log files in ${dataset_dir})"
            continue
        fi

        # Duyệt qua từng file log
        for log_file in "${log_files[@]}"; do
            ((total_files++))
            echo "----------------------------------------------------------"

            # Gọi script python truyền đường dẫn file log vào tham số --input
            python3 "$PYTHON_SCRIPT" --input "$log_file"

            # Kiểm tra mã thoát (exit code) của lệnh python
            if [ $? -eq 0 ]; then
                ((success_count++))
            else
                ((failed_count++))
                echo "      [X] Error when processing: $log_file"
            fi
        done
    done
done

echo ""
echo "=========================================================="
echo "FINISHED!"
echo "Total files processed : $total_files"
echo "Successful         : $success_count"
echo "Failed           : $failed_count"
echo "=========================================================="