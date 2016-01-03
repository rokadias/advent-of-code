namespace Advent

open System
open System.Collections.Generic
open System.IO
open System.Text.RegularExpressions

[<AutoOpen>]
module Helper =
    let readLines (filePath:string) = seq {
        use sr = new StreamReader(filePath)
        while not sr.EndOfStream do
            yield sr.ReadLine()
    }

    type IDictionary<'k, 'v> with
        member this.GetOrDefault (key:'k) (defaultValue:'v) =
            let mutable value = defaultValue
            if this.TryGetValue(key, &value) then
                value
            else
                defaultValue

    let (|Regex|_|) pattern input =
        let m = Regex.Match(input, pattern)
        if m.Success then Some(List.tail [ for g in m.Groups -> g.Value ])
        else None
