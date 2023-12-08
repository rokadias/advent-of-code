namespace Advent

open System
open System.Collections.Generic
open System.IO

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
