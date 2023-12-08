namespace charExpansion

open System
open System.Linq
open System.Text
open System.Text.RegularExpressions
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let lines = Helper.readLines(argv.[0])

        let hexReplace (m : Match) =
            let hex = m.Groups.[1].Value
            let value = Convert.ToInt32(hex, 16)
            Char.ConvertFromUtf32 value

        let fixString (str:string) =
            let mutable result =
                str.Replace(@"\", @"\\")
            result <- result.Replace("\"", "\\\"")
            "\"" +  result + "\""

        let originalSum =
            Seq.map (fun (line : string) -> line.Length) lines
            |> Seq.sum

        let newSum =
            Seq.map fixString lines
            |> Seq.map (fun (line : string) -> line.Length)
            |> Seq.sum

        printfn "originalSum: %d" originalSum
        printfn "newSum: %d" newSum
        printfn "difference: %d" (newSum - originalSum)
        0
