use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;

const INPUT_FILE_PATH: &str = "input.txt";

fn main() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("src").join(INPUT_FILE_PATH);
    let contents = fs::read_to_string(path).expect("Should have found and read file");

    let lines = contents.split("\n");
    let mut left = Vec::new();
    let mut right: HashMap<i32, i32> = HashMap::new();
    lines.enumerate().for_each(|(_i, line)| {
        let args = line.split(" ");
        args.enumerate().for_each(|(i, arg)| {
            if !arg.is_empty() {
                let val = arg.parse::<i32>().unwrap();
                if i == 0 {
                    left.push(val);
                } else {
                    right.entry(val).and_modify(|counter| *counter += 1).or_insert(1);
                }
            }

        });
    });

    let similarities = left.iter().map(|val| { val * *right.get(&val).unwrap_or(&0) }).collect::<Vec<i32>>();

    let total: i32 = similarities.iter().sum();
    println!("Total Similarities: {}", total);
}
