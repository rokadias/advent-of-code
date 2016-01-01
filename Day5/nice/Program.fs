namespace nice

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let lines = Helper.readLines(argv.[0])
        let isVowel char =
            match char with
                | 'a' | 'e' | 'i' | 'o' | 'u' -> true
                | c -> false

        let duplicateChars index (input:string) =
            let currentChar = input.Chars index
            currentChar = input.Chars(index + 1)

        let naughtyChars index (input:string) =
            let currentChar = input.Chars index
            let combination = (string currentChar) + (string (input.Chars(index + 1)))
            match combination with
                | "ab" | "cd" | "pq" | "xy" -> true
                | n -> false

        let isNice (str:string) =
            let vowels =
                seq { 0 .. str.Length - 1 }
                |> Seq.filter (fun i -> isVowel(str.Chars(i)))
            if vowels.Count() < 3 then
                false
            else
                let doesDuplicate =
                    seq { 0 .. str.Length - 2 }
                    |> Seq.tryFind (fun i -> duplicateChars i str)
                if doesDuplicate = None then
                    false
                else
                    let hasNaughty =
                        seq { 0 .. str.Length - 2 }
                        |> Seq.tryFind (fun i -> naughtyChars i str)

                    hasNaughty = None

        let niceLines = lines |> Seq.filter isNice

        printfn "Nice Lines = %d" (niceLines.Count())
        printfn "All Lines = %d" (lines.Count())
        0
