namespace lookAndSay

open System
open System.Linq
open System.Text
open System.Text.RegularExpressions
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let chars = Helper.readLines(argv.[0]).First()

        let numberReplace (m : Match) =
            let digitCount = m.Groups.[0].Value.Length
            let digit = m.Groups.[1].Value
            (string digitCount) + digit

        let lookAndSay line =
            Regex.Replace(line, "(\d)\1*", new MatchEvaluator(numberReplace))

        let result =
            seq { 1 .. 40 }
            |> Seq.fold (fun line index -> lookAndSay line) chars
        printfn "Result Length = %d" result.Length
        0
