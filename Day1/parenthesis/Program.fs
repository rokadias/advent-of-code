namespace parenthesis

open System
open System.Linq
open Advent

module Program =
    [<EntryPoint>]
    let main argv =
        let chars = Helper.readLines(argv.[0]).First()
        let openCount = chars |> Seq.filter (fun c -> c = '(') |> Seq.length
        let closeCount = chars |> Seq.filter (fun c -> c = ')') |> Seq.length
        let diff = (openCount - closeCount)
        printfn "Open Count: %d" openCount
        printfn "Closed Count: %d" closeCount
        printfn "Diff = %d" diff
        0
