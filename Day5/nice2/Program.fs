namespace nice

open System
open System.Collections.Generic
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let lines = Helper.readLines(argv.[0])

        let buildDictionary index (input:string) (dict:IDictionary<string, int>) =
            let combine = (string (input.Chars(index))) + (string (input.Chars(index + 1)))
            let existingValue = dict.GetOrDefault combine 0
            let shouldIncrement =
                if index < input.Length - 3 then
                    let nextCombine = (string (input.Chars(index + 1))) + (string (input.Chars(index + 2)))
                    combine <> nextCombine
                else
                    true

            if shouldIncrement then
                dict.[combine] <- existingValue + 1

        let repeatCharacters index (input:string) =
            let currentChar = input.Chars index
            let compareChar = input.Chars (index + 2)
            compareChar = currentChar

        let isNice (str:string) =
            let dictionary = new Dictionary<string, int>()
            seq { 0 .. str.Length - 2 }
            |> Seq.iter (fun i -> buildDictionary i str dictionary)
            let valueIsBelowTwo (kvp:KeyValuePair<string, int>) =
                kvp.Value < 2
            if Seq.forall valueIsBelowTwo dictionary then
                false
            else
                let doesRepeat =
                    seq { 0 .. str.Length - 3 }
                    |> Seq.tryFind (fun i -> repeatCharacters i str)
                doesRepeat <> None

        let niceLines = lines |> Seq.filter isNice

        printfn "Nice Lines = %d" (niceLines.Count())
        printfn "All Lines = %d" (lines.Count())
        0
