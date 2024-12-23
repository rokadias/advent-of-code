use std::env;
use std::fs;
use std::path::Path;

const INPUT_FILE_PATH: &str = "input.txt";

fn main() {
    let path = Path::new(env!("CARGO_MANIFEST_DIR")).join("src").join(INPUT_FILE_PATH);
    let contents = fs::read_to_string(path).expect("Should have found and read file");

    let lines = contents.split("\n");
    let mut left = Vec::new();
    let mut right = Vec::new();
    lines.enumerate().for_each(|(_i, line)| {
        let args = line.split(" ");
        args.enumerate().for_each(|(i, arg)| {
            if !arg.is_empty() {
                let val = arg.parse::<i32>().unwrap();
                if i == 0 {
                    left.push(val);
                } else {
                    right.push(val);
                }
            }

        });
    });

    left.sort();
    right.sort();

    let mut deltas = Vec::new();

    for (i, (l, r)) in left.iter().zip(right.iter()).enumerate() {
        let delta = l - r;
        let absolute_delta = delta.abs();
        deltas.push(absolute_delta);
    }

    let total: i32 = deltas.iter().sum();
    println!("Total: {}", total);
}
