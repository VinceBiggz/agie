#!/usr/bin/env python3
"""
AGIE - AI Governance Intelligence Engine

Command-line interface for AI governance risk assessment.

@author: Vincent Wachira
@date: 2025-02-15
@version: 0.1.0
@license: MIT
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from src.logger import logger
from src.parsers.csv_parser import CSVParser, CSVParserError
from src.analyser.gemini_client import GeminiClient, GeminiClientError
from src.analyser.risk_analyser import Riskanalyser, RiskanalyserError
from src.outputs.markdown_report import MarkdownReportGenerator

console = Console()


@click.group()
@click.version_option(version='0.1.0', prog_name='AGIE')
def cli():
    """
    AGIE - AI Governance Intelligence Engine
    
    Analyse AI governance risks against ISO 27001 standards.
    """
    pass


@cli.command()
@click.option(
    '--risk-register',
    '-r',
    required=True,
    type=click.Path(exists=True),
    help='Path to CSV risk register file'
)
@click.option(
    '--use-case',
    '-u',
    required=True,
    help='Description of AI use case to analyse'
)
@click.option(
    '--output',
    '-o',
    default='agie_report.md',
    type=click.Path(),
    help='Output report file path (default: agie_report.md)'
)
@click.option(
    '--context',
    '-c',
    help='Additional context (e.g., "industry: financial services")'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose output'
)
def analyse(risk_register, use_case, output, context, verbose):
    """
    Analyse AI governance risks and generate report.
    
    Example:
    
        agie analyse -r data/risks.csv -u "Deploy AI chatbot for customer support"
    """
    try:
        # Show header
        console.print()
        console.print(Panel.fit(
            "[bold cyan]AGIE - AI Governance Intelligence Engine[/bold cyan]\n"
            "[dim]Analysing AI risks against ISO 27001 standards...[/dim]",
            border_style="cyan"
        ))
        console.print()
        
        # Parse context if provided
        context_dict = None
        if context:
            # Simple key:value parsing
            context_dict = {}
            for pair in context.split(','):
                if ':' in pair:
                    key, value = pair.split(':', 1)
                    context_dict[key.strip()] = value.strip()
        
        # Step 1: Initialize analyser
        with console.status("[bold green]Initialising analyser...") as status:
            analyser = Riskanalyser()
            console.print("✓ Analyser ready", style="green")
        
        # Step 2: Run analysis
        with console.status("[bold yellow]Analysing risks (this may take 15-30 seconds)...") as status:
            assessment = analyser.analyse(
                risk_register_path=risk_register,
                use_case_description=use_case,
                context=context_dict
            )
            console.print("✓ Analysis complete", style="green")
        
        # Step 3: Display summary
        console.print()
        _display_summary(assessment)
        
        # Step 4: Generate report
        with console.status(f"[bold blue]Generating report: {output}...") as status:
            generator = MarkdownReportGenerator()
            report_path = generator.generate(assessment, output_path=output)
            console.print(f"✓ Report saved: [bold]{report_path}[/bold]", style="green")
        
        # Success message
        console.print()
        console.print(Panel.fit(
            f"[bold green]✓ Analysis Complete![/bold green]\n\n"
            f"Report: [cyan]{report_path}[/cyan]\n"
            f"Risk Score: [yellow]{assessment.summary_statistics['overall_risk_score']:.1f}/10[/yellow]\n"
            f"High-Priority Items: [red]{len(assessment.high_priority_items)}[/red]",
            border_style="green"
        ))
        console.print()
        
    except CSVParserError as e:
        console.print(f"\n[bold red]✗ CSV Parsing Error:[/bold red] {e}\n", style="red")
        logger.error(f"CSV parsing failed: {e}")
        sys.exit(1)
        
    except GeminiClientError as e:
        console.print(f"\n[bold red]✗ AI Analysis Error:[/bold red] {e}\n", style="red")
        console.print("[dim]Hint: Check your GOOGLE_API_KEY in .env file[/dim]\n")
        logger.error(f"Gemini API failed: {e}")
        sys.exit(1)
        
    except RiskanalyserError as e:
        console.print(f"\n[bold red]✗ Analysis Error:[/bold red] {e}\n", style="red")
        logger.error(f"Analysis failed: {e}")
        sys.exit(1)
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Unexpected Error:[/bold red] {e}\n", style="red")
        logger.critical(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


@cli.command()
@click.argument('risk_register', type=click.Path(exists=True))
def validate(risk_register):
    """
    Validate risk register CSV format.
    
    Example:
    
        agie validate data/risks.csv
    """
    try:
        console.print()
        console.print("[bold cyan]Validating risk register...[/bold cyan]\n")
        
        parser = CSVParser()
        df = parser.parse(risk_register)
        summary = parser.get_summary(df)
        
        # Display validation results
        table = Table(title="Validation Results", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Risks", str(summary['total_risks']))
        table.add_row("Average Likelihood", f"{summary['average_likelihood']:.2f}")
        table.add_row("Average Impact", f"{summary['average_impact']:.2f}")
        table.add_row("Average Risk Score", f"{summary['average_risk_score']:.2f}")
        table.add_row("High Risk Items", str(summary['high_risk_count']))
        table.add_row("Columns", ", ".join(summary['columns']))
        
        console.print(table)
        console.print()
        console.print("[bold green]✓ Risk register is valid![/bold green]\n")
        
    except CSVParserError as e:
        console.print(f"[bold red]✗ Validation Failed:[/bold red] {e}\n", style="red")
        sys.exit(1)


@cli.command()
def version():
    """Show version information."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]AGIE v0.1.0[/bold cyan]\n\n"
        "AI Governance Intelligence Engine\n"
        "[dim]Built with ❤️ for IT leaders and CISOs[/dim]\n\n"
        "Author: Vincent Wachira Kung'u\n"
        "License: MIT\n"
        "GitHub: github.com/VinceBiggz/agie",
        border_style="cyan"
    ))
    console.print()


@cli.command()
def examples():
    """Show usage examples."""
    console.print()
    console.print(Panel(
        "[bold cyan]AGIE Usage Examples[/bold cyan]\n\n"
        
        "[bold]1. Basic Analysis:[/bold]\n"
        "[green]agie analyse -r data/risks.csv -u \"Deploy AI chatbot\"[/green]\n\n"
        
        "[bold]2. With Context:[/bold]\n"
        "[green]agie analyse -r data/risks.csv -u \"AI for loan approvals\" "
        "-c \"industry: financial services, data: PII\"[/green]\n\n"
        
        "[bold]3. Custom Output:[/bold]\n"
        "[green]agie analyse -r data/risks.csv -u \"Resume screening AI\" "
        "-o reports/hr_analysis.md[/green]\n\n"
        
        "[bold]4. Validate CSV:[/bold]\n"
        "[green]agie validate data/risks.csv[/green]\n\n"
        
        "[bold]5. Verbose Mode:[/bold]\n"
        "[green]agie analyse -r data/risks.csv -u \"Fraud detection\" -v[/green]",
        border_style="cyan",
        padding=(1, 2)
    ))
    console.print()


def _display_summary(assessment):
    """Display analysis summary in terminal."""
    stats = assessment.summary_statistics
    
    # Summary table
    table = Table(title="Analysis Summary", show_header=True, border_style="cyan")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")
    
    table.add_row("Overall Risk Score", f"{stats['overall_risk_score']:.1f}/10")
    table.add_row("Organisational Risks", str(stats['total_organizational_risks']))
    table.add_row("AI-Specific Risks", str(stats['total_ai_risks']))
    table.add_row("Governance Gaps", str(stats['total_governance_gaps']))
    table.add_row("ISO 27001 Domains", str(stats['iso_domains_affected']))
    table.add_row("High-Priority Items", str(stats['high_risk_items']))
    
    console.print(table)
    console.print()
    
    # Top risks preview
    if assessment.high_priority_items:
        console.print("[bold cyan]Top Priority Actions:[/bold cyan]")
        for i, item in enumerate(assessment.high_priority_items[:3], 1):
            priority_color = "red" if item['priority'] == 'HIGH' else "yellow"
            console.print(
                f"  {i}. [{priority_color}]{item['priority']}[/{priority_color}] "
                f"{item['risk_id']}: {item['description'][:60]}..."
            )
        console.print()


if __name__ == '__main__':
    cli()