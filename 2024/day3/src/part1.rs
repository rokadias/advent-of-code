use std::env;
use std::fs;
use std::path::Path;
use regex::Regex;

const INPUT_FILE_PATH: &str = "input.txt";

fn main() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("src").join(INPUT_FILE_PATH);
    let contents = fs::read_to_string(path).expect("Should have found and read file");
    let re = Regex::new(r"mul\(([0-9]+),([0-9]+)\)").unwrap();
    let mut muls = vec![]; 

    for cap in re.captures_iter(&contents) {
        let first_value = cap.get(1).unwrap().as_str().parse::<i32>().unwrap();
        let second_value = cap.get(2).unwrap().as_str().parse::<i32>().unwrap();

        muls.push(first_value * second_value);
    }

    let total: i32 = muls.iter().sum();
    println!("Total: {}", total);
}

