namespace jsonSum

open System
open System.Linq
open System.Text.RegularExpressions
open Advent
open FSharp.Data
open FSharp.Data.JsonExtensions

module Program =
    [<EntryPoint>]
    let main argv =
        let line = Helper.readLines(argv.[0]).First()

        let safeGet f =
            try
                Some(f())
            with
                | ex -> None

        let isOtherType (value : JsonValue) =
            let meetsType f =
                safeGet f |> Option.isSome
            let otherTypes =
                [
                 meetsType value.AsBoolean;
                 meetsType value.AsDateTime;
                 meetsType value.AsDecimal;
                 meetsType value.AsFloat;
                 meetsType value.AsGuid;
                 meetsType value.AsString
                 ]
            Seq.exists id otherTypes

        let rec evaluate (value : JsonValue) sum =
            let arr = safeGet value.AsArray
            let i = safeGet value.AsInteger
            
                 
            if (Option.isSome arr) && arr.Value.Length > 0 then
                Seq.fold (fun acc (v : JsonValue) -> evaluate v acc) sum arr.Value
            elif Option.isSome i then
                sum + (Option.get i)
            elif isOtherType value then
                sum
            else
                let checkForRedString (tup : string * JsonValue) =
                    (safeGet (snd tup).AsString) = Some("red")
                    
                if Seq.exists checkForRedString value.Properties then
                    sum
                else
                    Seq.fold (fun acc tup -> evaluate (snd tup) acc) sum value.Properties

        let parsed = JsonValue.Parse(line)
        printfn "Json Sum: %d" (evaluate parsed 0)
        0
