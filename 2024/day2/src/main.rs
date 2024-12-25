use std::env;
use std::fs;
use std::path::Path;

const INPUT_FILE_PATH: &str = "input.txt";

fn main() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("src").join(INPUT_FILE_PATH);
    let contents = fs::read_to_string(path).expect("Should have found and read file");

    let lines = contents.split("\n");
    let mut input = Vec::new();
    lines.enumerate().for_each(|(_i, line)| {
        let mut lineVec = Vec::new();
        let args = line.split(" ");
        args.enumerate().for_each(|(_j, arg)| {
            if !arg.is_empty() {
                let val = arg.parse::<i32>().unwrap();
                lineVec.push(val);
            }
        });

        if !lineVec.is_empty() {
            input.push(lineVec);
        }
    });

    let checks: Vec<_> = input.iter().map(checkReportWithOneFailure).collect();
    println!("checks: {:?}", checks);
    let total: i32 = checks.iter().sum();
    println!("Total: {}", total);
}

fn checkReportWithOneFailure(report: &Vec<i32>) -> i32 {
    let (return_value, position) = checkReport(report);
    if position == 0 {
        return return_value;
    }
    println!("report: {:?}", report);


    let mut n_replaced_vec = report.to_vec();
    let mut n_minus_1_replaced_vec = report.to_vec();
    let mut first_replace = report.to_vec();

    n_replaced_vec.remove(position);
    n_minus_1_replaced_vec.remove(position - 1);
    first_replace.remove(0usize);

    let n_check = checkReport(&n_replaced_vec);
    let n_minus_1_check = checkReport(&n_minus_1_replaced_vec);
    let first_replace_check = checkReport(&first_replace);

    return n_check.0 | n_minus_1_check.0 | first_replace_check.0;
}

fn checkReport(report: &Vec<i32>) -> (i32, usize) {
    if report.len() < 2 {
        return (0, 0);
    }

    let mut is_increasing = None;
    for n in 1..report.len() {
        if report[n] == report[n -1] {
            return (0, n);
        }
        
        match is_increasing {
            Some(increasing) => {
                if increasing {
                    if report[n] < report[n -1] {
                        return (0, n);
                    }
                } else {
                    if report[n] > report[n -1] {
                        return (0, n);
                    }
                }
            },
            None => {
                if report[n] > report[n -1] {
                    is_increasing = Some(true);
                } else if report[n] < report[n -1] {
                    is_increasing = Some(false);
                }
            }
        }

        let difference = report[n] - report[n - 1];
        if difference.abs() > 3 {
            return (0, n);
        }
    }

    return (1, 0);
}
