#r "nuget: Newtonsoft.Json"
#r "nuget: System.Runtime.Caching"
#r @"C:/Windows/Microsoft.NET/Framework/v4.0.30319/System.Windows.Forms.dll"


open System
open System.IO
open System.Resources
open System.Collections
type FilePath = string

let readFile (filePath: FilePath) : ResXDataNode list =
    use reader = new ResXResourceReader(filePath, UseResXDataNodes = true)
    reader
    |> Seq.cast
    |> Seq.map (fun (x: DictionaryEntry) -> x.Value :?> ResXDataNode)
    |> Seq.toList

let resxFilesInDir path =
    Directory.EnumerateFiles(path, "*.*.resx")
    |> Seq.map (fun x -> (x, readFile x))

let nbMissingKeys (path: String) (refNodes: list<ResXDataNode>) (nodes:list<ResXDataNode>) =
    printf "\nMissing key analysis for : %s" path
    let toCheck = nodes |> List.map (fun x -> x.Name)
    let refs = refNodes |> List.map (fun x -> x.Name)
    refs
    |> List.except toCheck
    |> List.map (fun x -> printf "\nmissing key -> %s" x)
    |> List.length

let emptyArray : Reflection.AssemblyName[] = null

let nbNullValues (path: String) (nodes:list<ResXDataNode>) =
    printf "\nNull value analysis for : %s" path
    nodes
    |> List.filter (fun x -> String.IsNullOrEmpty(downcast x.GetValue(emptyArray)))
    |> List.map (fun x -> printf "\n null value -> %s" x.Name)
    |> List.length

let printValues (nodes:list<ResXDataNode>) =
    nodes
    |> List.iter (fun x -> printf "\nValue : %s" (downcast x.GetValue(emptyArray)))

let (+/) path1 path2 = Path.Combine(path1, path2)

let main =
    let args : string array = fsi.CommandLineArgs |> Array.tail
    if args.Length = 0 then failwith "Arguments : path-to-resx-dir name-of-base-resx"
    if String.IsNullOrEmpty(args.[0]) then failwith "1st arg is null. Please provide a PATH where resx files are located" 
    if String.IsNullOrEmpty(args.[1]) then failwith "2nd arg is null. Please provide the name of the resx file that act as base file"
    System.IO.Directory.SetCurrentDirectory (args.[0]) 
    let mainresx = readFile(args.[1])
    printf "\n\nen-US has %i elements" mainresx.Length

    let resxes = resxFilesInDir "."
    
    resxes
    |> Seq.iter (fun (a,b) -> printf "\npath : %s, with %i entries" a b.Length)
    
    let issuesNull = resxes
                    |> Seq.filter (fun (a,b) -> nbNullValues a b <> 0 )
    

    let issuesMissing = resxes
                        |> Seq.filter (fun (a,b) -> nbMissingKeys a mainresx b <> 0 )
    let nbIssues = issuesNull
                    |> Seq.append issuesMissing
                    |> Seq.length
    if nbIssues > 0 then failwith "Issues detected !"
    
