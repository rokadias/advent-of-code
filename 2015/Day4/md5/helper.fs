namespace Advent

open System
open System.IO

[<AutoOpen>]
module Helper =
    let readLines (filePath:string) = seq {
        use sr = new StreamReader(filePath)
        while not sr.EndOfStream do
            yield sr.ReadLine()
    }
