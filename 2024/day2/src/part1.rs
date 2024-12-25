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

    input.iter().enumerate().for_each(|(_i, l)| {
        println!("Line: {:?}", l);
    });

    let checks: Vec<_> = input.iter().map(checkReport).collect();
    println!("checks: {:?}", checks);
    let total: i32 = checks.iter().sum();
    println!("Total: {}", total);
}

fn checkReport(report: &Vec<i32>) -> i32 {
    if report.len() < 2 {
        return 0;
    }

    let mut is_increasing = None;
    for n in 1..report.len() {
        if report[n] == report[n -1] {
            return 0;
        }
        
        match is_increasing {
            Some(increasing) => {
                if increasing {
                    if report[n] < report[n -1] {
                        return 0;
                    }
                } else {
                    if report[n] > report[n -1] {
                        return 0;
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
            return 0;
        }
    }

    return 1;
}
